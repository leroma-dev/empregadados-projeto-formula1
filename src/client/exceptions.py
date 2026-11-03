"""Exceções personalizadas para o cliente OpenF1 API."""


class OpenF1Error(Exception):
    """Exceção base para erros relacionados à OpenF1 API."""

    def __init__(self, message: str, status_code: int | None = None) -> None:
        super().__init__(message)
        self.status_code = status_code


class RateLimitExceededError(OpenF1Error):
    """Lançada quando a cota de requisições por segundo/minuto é excedida."""


class ResourceNotFoundError(OpenF1Error):
    """Lançada quando um recurso solicitado não é encontrado (HTTP 404 ou vazio)."""


class SessionNotFoundError(ResourceNotFoundError):
    """Lançada especificamente quando uma sessão não é encontrada."""


class APIConnectionError(OpenF1Error):
    """Lançada em falhas de conexão ou timeout com a OpenF1 API."""
