"""Cliente de endpoints especializados da OpenF1 API."""

from typing import Any

from src.client.base import BaseClient


class OpenF1Client(BaseClient):
    """Cliente OpenF1 com métodos específicos para cada endpoint da API."""

    def get_meetings(
        self,
        year: int | None = None,
        meeting_key: int | str | None = None,
        country_name: str | None = None,
    ) -> list[dict[str, Any]]:
        """Retorna lista de Grandes Prêmios e eventos."""
        params: dict[str, Any] = {
            "year": year,
            "meeting_key": meeting_key,
            "country_name": country_name,
        }
        return self._get("meetings", params)

    def get_sessions(
        self,
        meeting_key: int | str | None = None,
        session_name: str | None = None,
        session_key: int | str | None = None,
        year: int | None = None,
        session_type: str | None = None,
    ) -> list[dict[str, Any]]:
        """Retorna sessões específicas de um GP (FP1, Quali, Race, etc.)."""
        params: dict[str, Any] = {
            "meeting_key": meeting_key,
            "session_name": session_name,
            "session_key": session_key,
            "year": year,
            "session_type": session_type,
        }
        return self._get("sessions", params)

    def get_drivers(
        self,
        session_key: int | str | None = None,
        driver_number: int | None = None,
        team_name: str | None = None,
    ) -> list[dict[str, Any]]:
        """Retorna lista de pilotos cadastrados em uma sessão."""
        params: dict[str, Any] = {
            "session_key": session_key,
            "driver_number": driver_number,
            "team_name": team_name,
        }
        return self._get("drivers", params)

    def get_laps(
        self,
        session_key: int | str | None = None,
        driver_number: int | None = None,
        lap_number: int | str | None = None,
    ) -> list[dict[str, Any]]:
        """Retorna tempos de voltas e parciais dos setores."""
        params: dict[str, Any] = {
            "session_key": session_key,
            "driver_number": driver_number,
            "lap_number": lap_number,
        }
        return self._get("laps", params)

    def get_car_data(
        self,
        session_key: int | str | None = None,
        driver_number: int | None = None,
        speed: str | int | None = None,
        date_start: str | None = None,
        date_end: str | None = None,
    ) -> list[dict[str, Any]]:
        """Retorna telemetria de alta frequência do carro."""
        params: dict[str, Any] = {
            "session_key": session_key,
            "driver_number": driver_number,
            "speed": speed,
            "date>=": date_start,
            "date<=": date_end,
        }
        return self._get("car_data", params)

    def get_location(
        self,
        session_key: int | str | None = None,
        driver_number: int | None = None,
        date: str | None = None,
    ) -> list[dict[str, Any]]:
        """Retorna coordenadas espaciais (x, y, z) dos carros no circuito."""
        params: dict[str, Any] = {
            "session_key": session_key,
            "driver_number": driver_number,
            "date": date,
        }
        return self._get("location", params)

    def get_intervals(
        self,
        session_key: int | str | None = None,
        driver_number: int | None = None,
        gap_to_leader: str | float | None = None,
    ) -> list[dict[str, Any]]:
        """Retorna intervalos de tempo entre carros e para o líder."""
        params: dict[str, Any] = {
            "session_key": session_key,
            "driver_number": driver_number,
            "gap_to_leader": gap_to_leader,
        }
        return self._get("intervals", params)

    def get_position(
        self,
        session_key: int | str | None = None,
        driver_number: int | None = None,
        position: int | str | None = None,
    ) -> list[dict[str, Any]]:
        """Retorna histórico de posições dos pilotos durante a sessão."""
        params: dict[str, Any] = {
            "session_key": session_key,
            "driver_number": driver_number,
            "position": position,
        }
        return self._get("position", params)

    def get_starting_grid(
        self,
        session_key: int | str | None = None,
        position: int | str | None = None,
        driver_number: int | None = None,
    ) -> list[dict[str, Any]]:
        """Retorna posições do grid de largada."""
        params: dict[str, Any] = {
            "session_key": session_key,
            "position": position,
            "driver_number": driver_number,
        }
        return self._get("starting_grid", params)

    def get_pit_stops(
        self,
        session_key: int | str | None = None,
        driver_number: int | None = None,
        lap_number: int | None = None,
    ) -> list[dict[str, Any]]:
        """Retorna paradas no pit stop e durações."""
        params: dict[str, Any] = {
            "session_key": session_key,
            "driver_number": driver_number,
            "lap_number": lap_number,
        }
        return self._get("pit", params)

    def get_stints(
        self,
        session_key: int | str | None = None,
        driver_number: int | None = None,
        compound: str | None = None,
    ) -> list[dict[str, Any]]:
        """Retorna informações de stints e compostos de pneus utilizados."""
        params: dict[str, Any] = {
            "session_key": session_key,
            "driver_number": driver_number,
            "compound": compound,
        }
        return self._get("stints", params)

    def get_race_control(
        self,
        session_key: int | str | None = None,
        flag: str | None = None,
        category: str | None = None,
        driver_number: int | None = None,
    ) -> list[dict[str, Any]]:
        """Retorna mensagens, bandeiras e alertas da direção de prova."""
        params: dict[str, Any] = {
            "session_key": session_key,
            "flag": flag,
            "category": category,
            "driver_number": driver_number,
        }
        return self._get("race_control", params)

    def get_weather(
        self,
        session_key: int | str | None = None,
        date: str | None = None,
    ) -> list[dict[str, Any]]:
        """Retorna registros de condições meteorológicas durante a sessão."""
        params: dict[str, Any] = {
            "session_key": session_key,
            "date": date,
        }
        return self._get("weather", params)

    def get_team_radio(
        self,
        session_key: int | str | None = None,
        driver_number: int | None = None,
    ) -> list[dict[str, Any]]:
        """Retorna registros e áudios de rádio de equipe."""
        params: dict[str, Any] = {
            "session_key": session_key,
            "driver_number": driver_number,
        }
        return self._get("team_radio", params)

    def get_session_results(
        self,
        session_key: int | str | None = None,
        position: int | str | None = None,
        driver_number: int | None = None,
    ) -> list[dict[str, Any]]:
        """Retorna resultado final e classificação oficial da sessão."""
        params: dict[str, Any] = {
            "session_key": session_key,
            "position": position,
            "driver_number": driver_number,
        }
        return self._get("session_result", params)

    def get_overtakes(
        self,
        session_key: int | str | None = None,
        driver_number: int | None = None,
    ) -> list[dict[str, Any]]:
        """Retorna histórico de ultrapassagens da sessão."""
        params: dict[str, Any] = {
            "session_key": session_key,
            "driver_number": driver_number,
        }
        return self._get("overtakes", params)
