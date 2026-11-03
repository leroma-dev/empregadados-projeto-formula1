"""Cliente base HTTP com controle de taxa (rate limiting) e retries para OpenF1."""

import random
import threading
import time
from collections import deque
from typing import Any

import httpx

from src.client.exceptions import (
    APIConnectionError,
    OpenF1Error,
    RateLimitExceededError,
    ResourceNotFoundError,
)


class RateLimiter:
    """Controlador de taxa em memória para respeitar o Community Tier da OpenF1.

    Limites oficiais:
    - Máximo de 3 requisições por segundo.
    - Máximo de 30 requisições por minuto.
    - Intervalo mínimo de 0.35s entre requisições consecutivas.
    """

    def __init__(
        self,
        max_per_second: int = 3,
        max_per_minute: int = 30,
        min_interval_seconds: float = 0.35,
    ) -> None:
        self.max_per_second = max_per_second
        self.max_per_minute = max_per_minute
        self.min_interval_seconds = min_interval_seconds

        self._second_queue: deque[float] = deque()
        self._minute_queue: deque[float] = deque()
        self._last_call_time: float = 0.0
        self._lock = threading.Lock()

    def acquire(self) -> None:
        """Aguarda, se necessário, para garantir que as cotas de taxa sejam respeitadas."""
        while True:
            with self._lock:
                now = time.monotonic()

                # Limpar requisições fora da janela de 1 segundo
                while self._second_queue and now - self._second_queue[0] >= 1.0:
                    self._second_queue.popleft()

                # Limpar requisições fora da janela de 60 segundos
                while self._minute_queue and now - self._minute_queue[0] >= 60.0:
                    self._minute_queue.popleft()

                wait_time = 0.0

                # 1. Checar intervalo mínimo
                elapsed_since_last = now - self._last_call_time
                if elapsed_since_last < self.min_interval_seconds:
                    wait_time = max(
                        wait_time, self.min_interval_seconds - elapsed_since_last
                    )

                # 2. Checar limite por segundo
                if len(self._second_queue) >= self.max_per_second:
                    oldest_sec = self._second_queue[0]
                    wait_time = max(wait_time, 1.0 - (now - oldest_sec))

                # 3. Checar limite por minuto
                if len(self._minute_queue) >= self.max_per_minute:
                    oldest_min = self._minute_queue[0]
                    wait_time = max(wait_time, 60.0 - (now - oldest_min))

                if wait_time <= 0.001:
                    actual_now = time.monotonic()
                    self._second_queue.append(actual_now)
                    self._minute_queue.append(actual_now)
                    self._last_call_time = actual_now
                    return

            time.sleep(wait_time)


class BaseClient:
    """Cliente HTTP base configurado com retries, timeouts e rate limiting."""

    BASE_URL = "https://api.openf1.org/v1"

    def __init__(
        self,
        base_url: str = BASE_URL,
        timeout: float = 15.0,
        rate_limiter: RateLimiter | None = None,
        max_retries: int = 3,
        backoff_factor: float = 1.0,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.rate_limiter = rate_limiter or RateLimiter()
        self.max_retries = max_retries
        self.backoff_factor = backoff_factor
        self._client: httpx.Client | None = None

    @property
    def client(self) -> httpx.Client:
        """Inicializa preguiçosamente o cliente HTTP."""
        if self._client is None:
            self._client = httpx.Client(
                timeout=httpx.Timeout(self.timeout),
                headers={
                    "Accept": "application/json",
                    "User-Agent": "OpenF1-Analytics/0.1.0",
                },
            )
        return self._client

    def _prepare_params(self, params: dict[str, Any] | None) -> list[tuple[str, str]]:
        """Converte dicionário de parâmetros ignorando nulos e tratando operadores."""
        if not params:
            return []
        query_params: list[tuple[str, str]] = []
        for key, value in params.items():
            if value is None:
                continue
            query_params.append((key, str(value)))
        return query_params

    def _get(
        self, endpoint: str, params: dict[str, Any] | None = None
    ) -> list[dict[str, Any]]:
        """Executa requisição GET com rate limiting e retry automático para HTTP 429."""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        query_params = self._prepare_params(params)

        for attempt in range(self.max_retries + 1):
            self.rate_limiter.acquire()
            try:
                response = self.client.get(url, params=query_params)
            except (
                httpx.ConnectError,
                httpx.TimeoutException,
                httpx.NetworkError,
            ) as err:
                if attempt == self.max_retries:
                    raise APIConnectionError(
                        f"Falha de conexão com OpenF1 ao acessar {endpoint}: {err}"
                    ) from err
                delay = self.backoff_factor * (2**attempt) + random.uniform(0.1, 0.4)
                time.sleep(delay)
                continue

            if response.status_code == 200:
                data = response.json()
                if isinstance(data, list):
                    return data
                if isinstance(data, dict):
                    return [data]
                return []

            if response.status_code == 404:
                raise ResourceNotFoundError(
                    f"Recurso não encontrado em {endpoint} (HTTP 404).",
                    status_code=404,
                )

            if response.status_code == 429:
                if attempt == self.max_retries:
                    raise RateLimitExceededError(
                        "Limite de requisições OpenF1 excedido (HTTP 429 após retries).",
                        status_code=429,
                    )
                # Respeita o cabeçalho Retry-After se fornecido
                retry_after_header = response.headers.get("Retry-After")
                if retry_after_header and retry_after_header.isdigit():
                    delay = float(retry_after_header)
                else:
                    delay = self.backoff_factor * (2**attempt) + random.uniform(
                        0.2, 0.6
                    )
                time.sleep(delay)
                continue

            if 500 <= response.status_code < 600:
                if attempt == self.max_retries:
                    raise APIConnectionError(
                        f"Erro do servidor OpenF1 (HTTP {response.status_code}): {response.text}",
                        status_code=response.status_code,
                    )
                delay = self.backoff_factor * (2**attempt) + random.uniform(0.2, 0.5)
                time.sleep(delay)
                continue

            raise OpenF1Error(
                f"Erro na requisição OpenF1 {endpoint} (HTTP {response.status_code}): {response.text}",
                status_code=response.status_code,
            )

        raise OpenF1Error(f"Falha ao executar requisição GET para {endpoint}.")

    def close(self) -> None:
        """Encerra a conexão do cliente HTTP."""
        if self._client is not None and not self._client.is_closed:
            self._client.close()

    def __enter__(self) -> "BaseClient":
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        self.close()
