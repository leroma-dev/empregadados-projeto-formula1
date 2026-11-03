"""Testes unitários para o cliente OpenF1, RateLimiter e tratamento de exceções."""

import time
from typing import Any
from unittest.mock import MagicMock

import httpx
import pytest

from src.client.base import BaseClient, RateLimiter
from src.client.endpoints import OpenF1Client
from src.client.exceptions import (
    APIConnectionError,
    OpenF1Error,
    RateLimitExceededError,
    ResourceNotFoundError,
)


class TestRateLimiter:
    """Testes para o controlador de taxa RateLimiter."""

    def test_init_defaults(self) -> None:
        limiter = RateLimiter(
            max_per_second=3, max_per_minute=30, min_interval_seconds=0.1
        )
        assert limiter.max_per_second == 3
        assert limiter.max_per_minute == 30
        assert limiter.min_interval_seconds == 0.1

    def test_acquire_single_call(self) -> None:
        limiter = RateLimiter(min_interval_seconds=0.01)
        start = time.monotonic()
        limiter.acquire()
        elapsed = time.monotonic() - start
        assert elapsed < 0.1

    def test_acquire_cleans_old_timestamps(self) -> None:
        limiter = RateLimiter(
            max_per_second=3, max_per_minute=30, min_interval_seconds=0.0
        )
        past_time = time.monotonic() - 70.0
        limiter._second_queue.append(past_time)
        limiter._minute_queue.append(past_time)

        limiter.acquire()
        assert past_time not in limiter._second_queue
        assert past_time not in limiter._minute_queue


class TestBaseClient:
    """Testes para o cliente HTTP base BaseClient."""

    def test_prepare_params(self) -> None:
        client = BaseClient()
        params = {"year": 2024, "country": "Brazil", "none_val": None}
        result = client._prepare_params(params)
        assert ("year", "2024") in result
        assert ("country", "Brazil") in result
        assert ("none_val", "None") not in result
        assert client._prepare_params(None) == []

    def test_get_success(self, mocker: Any) -> None:
        client = BaseClient(rate_limiter=RateLimiter(min_interval_seconds=0.0))
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = [{"id": 1}]

        mocker.patch.object(client.client, "get", return_value=mock_resp)
        data = client._get("meetings", {"year": 2024})

        assert data == [{"id": 1}]

    def test_get_single_dict_to_list(self, mocker: Any) -> None:
        client = BaseClient(rate_limiter=RateLimiter(min_interval_seconds=0.0))
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {"id": 1}

        mocker.patch.object(client.client, "get", return_value=mock_resp)
        data = client._get("sessions")
        assert data == [{"id": 1}]

    def test_get_404_raises_resource_not_found(self, mocker: Any) -> None:
        client = BaseClient(rate_limiter=RateLimiter(min_interval_seconds=0.0))
        mock_resp = MagicMock()
        mock_resp.status_code = 404

        mocker.patch.object(client.client, "get", return_value=mock_resp)
        with pytest.raises(ResourceNotFoundError):
            client._get("not_found_endpoint")

    def test_get_429_exhausted_raises_rate_limit(self, mocker: Any) -> None:
        client = BaseClient(
            rate_limiter=RateLimiter(min_interval_seconds=0.0),
            max_retries=1,
            backoff_factor=0.01,
        )
        mock_resp = MagicMock()
        mock_resp.status_code = 429
        mock_resp.headers = {"Retry-After": "0"}

        mocker.patch.object(client.client, "get", return_value=mock_resp)
        with pytest.raises(RateLimitExceededError):
            client._get("laps")

    def test_get_500_exhausted_raises_connection_error(self, mocker: Any) -> None:
        client = BaseClient(
            rate_limiter=RateLimiter(min_interval_seconds=0.0),
            max_retries=1,
            backoff_factor=0.01,
        )
        mock_resp = MagicMock()
        mock_resp.status_code = 500
        mock_resp.text = "Internal Server Error"

        mocker.patch.object(client.client, "get", return_value=mock_resp)
        with pytest.raises(APIConnectionError):
            client._get("weather")

    def test_get_network_error_exhausted(self, mocker: Any) -> None:
        client = BaseClient(
            rate_limiter=RateLimiter(min_interval_seconds=0.0),
            max_retries=1,
            backoff_factor=0.01,
        )
        mocker.patch.object(
            client.client, "get", side_effect=httpx.ConnectError("Network is down")
        )
        with pytest.raises(APIConnectionError):
            client._get("drivers")

    def test_get_unexpected_status(self, mocker: Any) -> None:
        client = BaseClient(rate_limiter=RateLimiter(min_interval_seconds=0.0))
        mock_resp = MagicMock()
        mock_resp.status_code = 400
        mock_resp.text = "Bad Request"

        mocker.patch.object(client.client, "get", return_value=mock_resp)
        with pytest.raises(OpenF1Error):
            client._get("car_data")

    def test_context_manager(self) -> None:
        with BaseClient() as c:
            assert c is not None
            client_ref = c.client
            assert not client_ref.is_closed
        assert client_ref.is_closed


class TestOpenF1ClientEndpoints:
    """Testes para os métodos especializados do OpenF1Client."""

    @pytest.fixture
    def client(self) -> OpenF1Client:
        return OpenF1Client(rate_limiter=RateLimiter(min_interval_seconds=0.0))

    def test_get_meetings(self, client: OpenF1Client, mocker: Any) -> None:
        mock_get = mocker.patch.object(
            client, "_get", return_value=[{"meeting_key": 1}]
        )
        res = client.get_meetings(year=2024, meeting_key=1, country_name="Bahrain")
        assert res == [{"meeting_key": 1}]
        mock_get.assert_called_once_with(
            "meetings", {"year": 2024, "meeting_key": 1, "country_name": "Bahrain"}
        )

    def test_get_sessions(self, client: OpenF1Client, mocker: Any) -> None:
        mock_get = mocker.patch.object(
            client, "_get", return_value=[{"session_key": 10}]
        )
        res = client.get_sessions(meeting_key=1, session_name="Race")
        assert res == [{"session_key": 10}]
        mock_get.assert_called_once()

    def test_get_drivers(self, client: OpenF1Client, mocker: Any) -> None:
        mock_get = mocker.patch.object(
            client, "_get", return_value=[{"driver_number": 1}]
        )
        res = client.get_drivers(session_key=10, driver_number=1)
        assert res == [{"driver_number": 1}]
        mock_get.assert_called_once()

    def test_get_laps(self, client: OpenF1Client, mocker: Any) -> None:
        mock_get = mocker.patch.object(client, "_get", return_value=[{"lap_number": 5}])
        res = client.get_laps(session_key=10, driver_number=1, lap_number=5)
        assert res == [{"lap_number": 5}]
        mock_get.assert_called_once()

    def test_get_car_data(self, client: OpenF1Client, mocker: Any) -> None:
        mock_get = mocker.patch.object(client, "_get", return_value=[{"speed": 310}])
        res = client.get_car_data(session_key=10, driver_number=1, speed=">=300")
        assert res == [{"speed": 310}]
        mock_get.assert_called_once()

    def test_get_other_endpoints(self, client: OpenF1Client, mocker: Any) -> None:
        mock_get = mocker.patch.object(client, "_get", return_value=[])

        client.get_location(session_key=10, driver_number=1)
        client.get_intervals(session_key=10, driver_number=1)
        client.get_position(session_key=10, driver_number=1)
        client.get_starting_grid(session_key=10, driver_number=1)
        client.get_pit_stops(session_key=10, driver_number=1)
        client.get_stints(session_key=10, driver_number=1)
        client.get_race_control(session_key=10, flag="YELLOW")
        client.get_weather(session_key=10)
        client.get_team_radio(session_key=10, driver_number=1)
        client.get_session_results(session_key=10, position=1)
        client.get_overtakes(session_key=10, driver_number=1)

        assert mock_get.call_count == 11
