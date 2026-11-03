"""Testes unitários para a camada de serviços e cálculos analíticos em src/services."""

from unittest.mock import MagicMock

from src.models import (
    CarData,
    Driver,
    Lap,
    SessionResult,
    Stint,
)
from src.services.session_service import SessionService
from src.services.stats_service import StatsService
from src.services.telemetry_service import TelemetryService


class TestSessionService:
    """Testes para o SessionService com mocks do OpenF1Client."""

    def test_get_meetings(self, sample_meetings_raw: list[dict]) -> None:
        mock_client = MagicMock()
        mock_client.get_meetings.return_value = sample_meetings_raw

        service = SessionService(client=mock_client)
        meetings = service.get_meetings(year=2024)

        assert len(meetings) == 2
        assert meetings[0].meeting_key == 1229
        mock_client.get_meetings.assert_called_once_with(year=2024)

    def test_get_sessions(self, sample_sessions_raw: list[dict]) -> None:
        mock_client = MagicMock()
        mock_client.get_sessions.return_value = sample_sessions_raw

        service = SessionService(client=mock_client)
        sessions = service.get_sessions(meeting_key=1229)

        assert len(sessions) == 2
        assert sessions[1].session_name == "Race"

    def test_get_drivers(self, sample_drivers_raw: list[dict]) -> None:
        mock_client = MagicMock()
        mock_client.get_drivers.return_value = sample_drivers_raw

        service = SessionService(client=mock_client)
        drivers = service.get_drivers(session_key=9478)

        assert len(drivers) == 3
        assert drivers[0].driver_number == 1

    def test_get_laps(self, sample_laps_raw: list[dict]) -> None:
        mock_client = MagicMock()
        mock_client.get_laps.return_value = sample_laps_raw

        service = SessionService(client=mock_client)
        laps = service.get_laps(session_key=9478, driver_number=1)

        assert len(laps) == 4
        assert laps[0].lap_number == 1

    def test_get_stints(self, sample_stints_raw: list[dict]) -> None:
        mock_client = MagicMock()
        mock_client.get_stints.return_value = sample_stints_raw

        service = SessionService(client=mock_client)
        stints = service.get_stints(session_key=9478)

        assert len(stints) == 2
        assert stints[0].compound == "SOFT"

    def test_get_results(self, sample_results_raw: list[dict]) -> None:
        mock_client = MagicMock()
        mock_client.get_session_results.return_value = sample_results_raw

        service = SessionService(client=mock_client)
        results = service.get_results(session_key=9478)

        assert len(results) == 3
        assert results[0].position == 1

    def test_get_weather(self, sample_weather_raw: list[dict]) -> None:
        mock_client = MagicMock()
        mock_client.get_weather.return_value = sample_weather_raw

        service = SessionService(client=mock_client)
        weather = service.get_weather(session_key=9478)

        assert len(weather) == 1
        assert weather[0].track_temperature == 29.8

    def test_get_car_data(self, sample_car_data_raw: list[dict]) -> None:
        mock_client = MagicMock()
        mock_client.get_car_data.return_value = sample_car_data_raw

        service = SessionService(client=mock_client)
        data = service.get_car_data(session_key=9478, driver_number=1)

        assert len(data) == 3
        assert data[0].speed == 250

    def test_get_session_summary(
        self,
        sample_drivers_raw: list[dict],
        sample_results_raw: list[dict],
        sample_weather_raw: list[dict],
    ) -> None:
        mock_client = MagicMock()
        mock_client.get_drivers.return_value = sample_drivers_raw
        mock_client.get_session_results.return_value = sample_results_raw
        mock_client.get_weather.return_value = sample_weather_raw

        service = SessionService(client=mock_client)
        summary = service.get_session_summary(session_key=9478)

        assert summary["total_drivers"] == 3
        assert summary["total_classified"] == 3
        assert summary["weather_points"] == 1


class TestStatsService:
    """Testes para o StatsService e métricas matemáticas."""

    def test_format_lap_time(self) -> None:
        assert StatsService.format_lap_time(None) == "--:--.---"
        assert StatsService.format_lap_time(-5.0) == "--:--.---"
        assert StatsService.format_lap_time(84.321) == "1:24.321"
        assert StatsService.format_lap_time(60.0) == "1:00.000"

    def test_get_fastest_lap(self, sample_laps_raw: list[dict]) -> None:
        laps = [Lap.model_validate(lap_raw) for lap_raw in sample_laps_raw]
        fastest = StatsService.get_fastest_lap(laps)
        assert fastest is not None
        assert fastest.driver_number == 1
        assert fastest.lap_number == 2
        assert fastest.lap_duration == 92.100

        assert StatsService.get_fastest_lap([]) is None

    def test_get_driver_fastest_lap(self, sample_laps_raw: list[dict]) -> None:
        laps = [Lap.model_validate(lap_raw) for lap_raw in sample_laps_raw]
        fl_16 = StatsService.get_driver_fastest_lap(laps, 16)
        assert fl_16 is not None
        assert fl_16.driver_number == 16
        assert fl_16.lap_duration == 93.400

    def test_get_fastest_sectors(self, sample_laps_raw: list[dict]) -> None:
        laps = [Lap.model_validate(lap_raw) for lap_raw in sample_laps_raw]
        sectors = StatsService.get_fastest_sectors(laps)

        assert sectors["s1"]["duration"] == 28.900
        assert sectors["s1"]["driver_number"] == 1

        assert sectors["s2"]["duration"] == 38.500
        assert sectors["s2"]["driver_number"] == 1

        assert sectors["s3"]["duration"] == 24.700
        assert sectors["s3"]["driver_number"] == 1

    def test_calculate_race_pace(self, sample_laps_raw: list[dict]) -> None:
        laps = [Lap.model_validate(lap_raw) for lap_raw in sample_laps_raw]
        pace = StatsService.calculate_race_pace(laps, driver_number=1)
        assert pace is not None
        # Média entre 94.5 e 92.1 = 93.3
        assert round(pace, 1) == 93.3

        assert StatsService.calculate_race_pace([], driver_number=99) is None

    def test_calculate_stint_statistics(
        self,
        sample_laps_raw: list[dict],
        sample_stints_raw: list[dict],
    ) -> None:
        laps = [Lap.model_validate(lap_raw) for lap_raw in sample_laps_raw]
        stints = [Stint.model_validate(s) for s in sample_stints_raw]

        stats = StatsService.calculate_stint_statistics(laps, stints)
        assert len(stats) == 2
        assert stats[0]["compound"] == "SOFT"
        assert stats[0]["total_laps"] == 18
        assert stats[0]["average_pace"] is not None

    def test_calculate_position_changes(
        self,
        sample_results_raw: list[dict],
        sample_drivers_raw: list[dict],
    ) -> None:
        results = [SessionResult.model_validate(r) for r in sample_results_raw]
        drivers = [Driver.model_validate(d) for d in sample_drivers_raw]

        changes = StatsService.calculate_position_changes(results, drivers)
        assert len(changes) == 3
        # Primeiro da lista deve ser o P1
        assert changes[0]["finish_position"] == 1
        assert changes[0]["position_change"] == 0

        # Segundo deve ser o Perez (largou em 5, chegou em 2 -> +3)
        assert changes[1]["driver_number"] == 11
        assert changes[1]["position_change"] == 3

    def test_calculate_teammate_comparison(
        self,
        sample_results_raw: list[dict],
        sample_drivers_raw: list[dict],
        sample_laps_raw: list[dict],
    ) -> None:
        results = [SessionResult.model_validate(r) for r in sample_results_raw]
        drivers = [Driver.model_validate(d) for d in sample_drivers_raw]
        laps = [Lap.model_validate(lap_raw) for lap_raw in sample_laps_raw]

        duels = StatsService.calculate_teammate_comparison(results, drivers, laps)
        assert len(duels) == 1
        assert duels[0]["team_name"] == "Red Bull Racing"
        assert duels[0]["driver_1"] in ["VER", "Max VERSTAPPEN"]
        assert duels[0]["driver_2"] in ["PER", "Sergio PEREZ"]


class TestTelemetryService:
    """Testes para o processamento de telemetria."""

    def test_to_dataframe_empty(self) -> None:
        df = TelemetryService.to_dataframe([])
        assert df.empty
        assert "speed" in df.columns
        assert "distance_m" in df.columns

    def test_to_dataframe_with_data(self, sample_car_data_raw: list[dict]) -> None:
        car_data = [CarData.model_validate(cd) for cd in sample_car_data_raw]
        df = TelemetryService.to_dataframe(car_data)

        assert len(df) == 3
        assert "time_sec" in df.columns
        assert "distance_m" in df.columns
        assert df["speed"].iloc[0] == 250
        assert df["distance_m"].iloc[-1] > 0

    def test_interpolate_to_distance(self, sample_car_data_raw: list[dict]) -> None:
        car_data = [CarData.model_validate(cd) for cd in sample_car_data_raw]
        df = TelemetryService.to_dataframe(car_data)
        interp_df = TelemetryService.interpolate_to_distance(df, num_points=100)

        assert len(interp_df) == 100
        assert "distance_m" in interp_df.columns
        assert "speed" in interp_df.columns

    def test_compare_laps(self, sample_car_data_raw: list[dict]) -> None:
        data_a = [CarData.model_validate(cd) for cd in sample_car_data_raw]
        # Criar dados b com velocidades ligeiramente menores
        raw_b = [dict(cd, speed=cd["speed"] - 10) for cd in sample_car_data_raw]
        data_b = [CarData.model_validate(cd) for cd in raw_b]

        comp_df = TelemetryService.compare_laps(
            data_a, data_b, label_a="VER", label_b="LEC", num_points=50
        )

        assert len(comp_df) == 50
        assert "speed_VER" in comp_df.columns
        assert "speed_LEC" in comp_df.columns
        assert "speed_delta" in comp_df.columns
        # Delta deve ser aproximadamente positivo (+10 km/h)
        assert comp_df["speed_delta"].mean() > 5.0
