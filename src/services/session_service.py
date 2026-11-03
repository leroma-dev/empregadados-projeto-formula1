"""Serviço de consolidação e extração hierárquica dos dados de sessão."""

from typing import Any

from src.client.endpoints import OpenF1Client
from src.models import (
    CarData,
    Driver,
    Lap,
    Meeting,
    Session,
    SessionResult,
    Stint,
    Weather,
)


class SessionService:
    """Gerencia a extração, conversão e agregação dos dados de sessões da OpenF1."""

    def __init__(self, client: OpenF1Client | None = None) -> None:
        self.client = client or OpenF1Client()

    def get_meetings(self, year: int = 2024) -> list[Meeting]:
        """Obtém e valida todos os Grandes Prêmios de um determinado ano."""
        raw_meetings = self.client.get_meetings(year=year)
        meetings = [Meeting.model_validate(m) for m in raw_meetings]
        # Ordenar por chave do evento ou data de início
        return sorted(meetings, key=lambda m: m.date_start or "")

    def get_sessions(self, meeting_key: int | str) -> list[Session]:
        """Obtém todas as sessões registradas para um Grande Prêmio."""
        raw_sessions = self.client.get_sessions(meeting_key=meeting_key)
        sessions = [Session.model_validate(s) for s in raw_sessions]
        return sorted(sessions, key=lambda s: s.date_start or "")

    def get_drivers(self, session_key: int | str) -> list[Driver]:
        """Obtém a lista de pilotos registrados em uma sessão."""
        raw_drivers = self.client.get_drivers(session_key=session_key)
        drivers = [Driver.model_validate(d) for d in raw_drivers]
        # Ordenar por número do piloto
        return sorted(drivers, key=lambda d: d.driver_number)

    def get_laps(
        self,
        session_key: int | str,
        driver_number: int | None = None,
    ) -> list[Lap]:
        """Obtém as voltas e parciais da sessão."""
        raw_laps = self.client.get_laps(
            session_key=session_key,
            driver_number=driver_number,
        )
        return [Lap.model_validate(lap) for lap in raw_laps]

    def get_stints(
        self,
        session_key: int | str,
        driver_number: int | None = None,
    ) -> list[Stint]:
        """Obtém o histórico de stints de pneus da sessão."""
        raw_stints = self.client.get_stints(
            session_key=session_key,
            driver_number=driver_number,
        )
        return [Stint.model_validate(stint) for stint in raw_stints]

    def get_results(self, session_key: int | str) -> list[SessionResult]:
        """Obtém os resultados e classificação oficial da sessão."""
        raw_results = self.client.get_session_results(session_key=session_key)
        results = [SessionResult.model_validate(r) for r in raw_results]
        return sorted(results, key=lambda r: (r.position is None, r.position or 999))

    def get_weather(self, session_key: int | str) -> list[Weather]:
        """Obtém as condições climáticas registradas na sessão."""
        raw_weather = self.client.get_weather(session_key=session_key)
        return [Weather.model_validate(w) for w in raw_weather]

    def get_car_data(
        self,
        session_key: int | str,
        driver_number: int,
        date_start: str | None = None,
        date_end: str | None = None,
    ) -> list[CarData]:
        """Obtém a telemetria em alta frequência filtrada por piloto e intervalo temporal."""
        raw_data = self.client.get_car_data(
            session_key=session_key,
            driver_number=driver_number,
            date_start=date_start,
            date_end=date_end,
        )
        return [CarData.model_validate(item) for item in raw_data]

    def get_session_summary(self, session_key: int | str) -> dict[str, Any]:
        """Gera um resumo consolidado da sessão."""
        drivers = self.get_drivers(session_key)
        results = self.get_results(session_key)
        weather = self.get_weather(session_key)

        return {
            "session_key": session_key,
            "total_drivers": len(drivers),
            "total_classified": len(results),
            "weather_points": len(weather),
            "drivers": drivers,
            "results": results,
        }
