"""Testes unitários para validação e schemas Pydantic v2 em src/models."""

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


class TestModels:
    """Validação e propriedades dos modelos de dados."""

    def test_meeting_model(self, sample_meetings_raw: list[dict]) -> None:
        meeting = Meeting.model_validate(sample_meetings_raw[0])
        assert meeting.meeting_key == 1229
        assert meeting.meeting_name == "Bahrain Grand Prix"
        assert meeting.year == 2024
        assert meeting.circuit_key == 63

    def test_session_model(self, sample_sessions_raw: list[dict]) -> None:
        session = Session.model_validate(sample_sessions_raw[1])
        assert session.session_key == 9478
        assert session.session_name == "Race"
        assert session.session_type == "Race"

    def test_driver_model_and_hex_colour(self, sample_drivers_raw: list[dict]) -> None:
        driver1 = Driver.model_validate(sample_drivers_raw[0])
        assert driver1.driver_number == 1
        assert driver1.full_name == "Max VERSTAPPEN"
        # Deve adicionar # caso não venha no JSON
        assert driver1.hex_colour == "#3671C6"

        driver2 = Driver.model_validate(sample_drivers_raw[1])
        assert driver2.hex_colour == "#3671C6"

        driver_no_colour = Driver(driver_number=99, full_name="Test Pilot")
        assert driver_no_colour.hex_colour == "#CCCCCC"

    def test_lap_model(self, sample_laps_raw: list[dict]) -> None:
        lap = Lap.model_validate(sample_laps_raw[0])
        assert lap.lap_number == 1
        assert lap.lap_duration == 94.500
        assert lap.duration_sector_1 == 29.500
        assert lap.is_pit_out_lap is False

    def test_stint_model_and_total_laps(self, sample_stints_raw: list[dict]) -> None:
        stint = Stint.model_validate(sample_stints_raw[0])
        assert stint.stint_number == 1
        assert stint.compound == "SOFT"
        assert stint.total_laps == 18

        stint_no_laps = Stint(session_key=1, driver_number=1, stint_number=1)
        assert stint_no_laps.total_laps == 0

    def test_car_data_model(self, sample_car_data_raw: list[dict]) -> None:
        car_data = CarData.model_validate(sample_car_data_raw[0])
        assert car_data.driver_number == 1
        assert car_data.speed == 250
        assert car_data.rpm == 10500
        assert car_data.throttle == 100
        assert car_data.brake == 0

    def test_session_result_and_position_change(
        self, sample_results_raw: list[dict]
    ) -> None:
        # P1 largou de P1 -> change = 0
        r1 = SessionResult.model_validate(sample_results_raw[0])
        assert r1.position == 1
        assert r1.grid_position == 1
        assert r1.position_change == 0

        # P2 largou de P5 -> change = +4
        r2 = SessionResult.model_validate(sample_results_raw[1])
        assert r2.position == 2
        assert r2.grid_position == 5
        assert r2.position_change == 3

        # P4 largou de P2 -> change = -2
        r3 = SessionResult.model_validate(sample_results_raw[2])
        assert r3.position == 4
        assert r3.grid_position == 2
        assert r3.position_change == -2

        r_no_grid = SessionResult(session_key=1, driver_number=1, position=3)
        assert r_no_grid.position_change is None

    def test_weather_model(self, sample_weather_raw: list[dict]) -> None:
        weather = Weather.model_validate(sample_weather_raw[0])
        assert weather.session_key == 9478
        assert weather.track_temperature == 29.8
        assert weather.air_temperature == 21.5
        assert weather.rainfall == 0
