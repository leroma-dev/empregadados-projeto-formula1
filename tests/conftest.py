"""Fixtures e mocks compartilhados para a suíte de testes com pytest."""

from typing import Any

import pytest


@pytest.fixture
def sample_meetings_raw() -> list[dict[str, Any]]:
    return [
        {
            "meeting_key": 1229,
            "meeting_name": "Bahrain Grand Prix",
            "meeting_official_name": "FORMULA 1 GULF AIR BAHRAIN GRAND PRIX 2024",
            "circuit_key": 63,
            "circuit_short_name": "Sakhir",
            "country_name": "Bahrain",
            "country_code": "BRN",
            "date_start": "2024-02-29T11:30:00+00:00",
            "gmt_offset": "+03:00",
            "year": 2024,
        },
        {
            "meeting_key": 1230,
            "meeting_name": "Saudi Arabian Grand Prix",
            "meeting_official_name": "FORMULA 1 STC SAUDI ARABIAN GRAND PRIX 2024",
            "circuit_key": 149,
            "circuit_short_name": "Jeddah",
            "country_name": "Saudi Arabia",
            "country_code": "KSA",
            "date_start": "2024-03-07T13:30:00+00:00",
            "gmt_offset": "+03:00",
            "year": 2024,
        },
    ]


@pytest.fixture
def sample_sessions_raw() -> list[dict[str, Any]]:
    return [
        {
            "session_key": 9472,
            "meeting_key": 1229,
            "session_name": "Practice 1",
            "session_type": "Practice",
            "date_start": "2024-02-29T11:30:00+00:00",
            "date_end": "2024-02-29T12:30:00+00:00",
            "gmt_offset": "+03:00",
            "year": 2024,
        },
        {
            "session_key": 9478,
            "meeting_key": 1229,
            "session_name": "Race",
            "session_type": "Race",
            "date_start": "2024-03-02T15:00:00+00:00",
            "date_end": "2024-03-02T17:00:00+00:00",
            "gmt_offset": "+03:00",
            "year": 2024,
        },
    ]


@pytest.fixture
def sample_drivers_raw() -> list[dict[str, Any]]:
    return [
        {
            "driver_number": 1,
            "broadcast_name": "M VERSTAPPEN",
            "full_name": "Max VERSTAPPEN",
            "name_acronym": "VER",
            "team_name": "Red Bull Racing",
            "team_colour": "3671C6",
            "headshot_url": "https://example.com/ver.png",
            "country_code": "NED",
            "session_key": 9478,
            "meeting_key": 1229,
        },
        {
            "driver_number": 11,
            "broadcast_name": "S PEREZ",
            "full_name": "Sergio PEREZ",
            "name_acronym": "PER",
            "team_name": "Red Bull Racing",
            "team_colour": "#3671C6",
            "headshot_url": "https://example.com/per.png",
            "country_code": "MEX",
            "session_key": 9478,
            "meeting_key": 1229,
        },
        {
            "driver_number": 16,
            "broadcast_name": "C LECLERC",
            "full_name": "Charles LECLERC",
            "name_acronym": "LEC",
            "team_name": "Ferrari",
            "team_colour": "E80020",
            "headshot_url": "https://example.com/lec.png",
            "country_code": "MON",
            "session_key": 9478,
            "meeting_key": 1229,
        },
    ]


@pytest.fixture
def sample_laps_raw() -> list[dict[str, Any]]:
    return [
        {
            "session_key": 9478,
            "meeting_key": 1229,
            "driver_number": 1,
            "lap_number": 1,
            "lap_duration": 94.500,
            "duration_sector_1": 29.500,
            "duration_sector_2": 39.200,
            "duration_sector_3": 25.800,
            "i1_speed": 295.0,
            "i2_speed": 280.0,
            "st_speed": 315.0,
            "is_pit_out_lap": False,
            "date_start": "2024-03-02T15:03:00+00:00",
        },
        {
            "session_key": 9478,
            "meeting_key": 1229,
            "driver_number": 1,
            "lap_number": 2,
            "lap_duration": 92.100,
            "duration_sector_1": 28.900,
            "duration_sector_2": 38.500,
            "duration_sector_3": 24.700,
            "i1_speed": 300.0,
            "i2_speed": 285.0,
            "st_speed": 320.0,
            "is_pit_out_lap": False,
            "date_start": "2024-03-02T15:04:32+00:00",
        },
        {
            "session_key": 9478,
            "meeting_key": 1229,
            "driver_number": 16,
            "lap_number": 1,
            "lap_duration": 95.200,
            "duration_sector_1": 30.100,
            "duration_sector_2": 39.500,
            "duration_sector_3": 25.600,
            "i1_speed": 292.0,
            "i2_speed": 278.0,
            "st_speed": 312.0,
            "is_pit_out_lap": False,
            "date_start": "2024-03-02T15:03:00+00:00",
        },
        {
            "session_key": 9478,
            "meeting_key": 1229,
            "driver_number": 16,
            "lap_number": 2,
            "lap_duration": 93.400,
            "duration_sector_1": 29.200,
            "duration_sector_2": 38.800,
            "duration_sector_3": 25.400,
            "i1_speed": 298.0,
            "i2_speed": 282.0,
            "st_speed": 316.0,
            "is_pit_out_lap": False,
            "date_start": "2024-03-02T15:04:35+00:00",
        },
    ]


@pytest.fixture
def sample_stints_raw() -> list[dict[str, Any]]:
    return [
        {
            "session_key": 9478,
            "meeting_key": 1229,
            "driver_number": 1,
            "stint_number": 1,
            "compound": "SOFT",
            "tyre_age_at_start": 0,
            "lap_start": 1,
            "lap_end": 18,
        },
        {
            "session_key": 9478,
            "meeting_key": 1229,
            "driver_number": 1,
            "stint_number": 2,
            "compound": "HARD",
            "tyre_age_at_start": 0,
            "lap_start": 19,
            "lap_end": 57,
        },
    ]


@pytest.fixture
def sample_results_raw() -> list[dict[str, Any]]:
    return [
        {
            "session_key": 9478,
            "meeting_key": 1229,
            "driver_number": 1,
            "position": 1,
            "grid_position": 1,
            "points": 26.0,
            "status": "Finished",
            "duration": 5460.5,
        },
        {
            "session_key": 9478,
            "meeting_key": 1229,
            "driver_number": 11,
            "position": 2,
            "grid_position": 5,
            "points": 18.0,
            "status": "Finished",
            "duration": 5482.9,
        },
        {
            "session_key": 9478,
            "meeting_key": 1229,
            "driver_number": 16,
            "position": 4,
            "grid_position": 2,
            "points": 12.0,
            "status": "Finished",
            "duration": 5500.1,
        },
    ]


@pytest.fixture
def sample_weather_raw() -> list[dict[str, Any]]:
    return [
        {
            "session_key": 9478,
            "date": "2024-03-02T15:00:00+00:00",
            "air_temperature": 21.5,
            "track_temperature": 29.8,
            "humidity": 45.0,
            "pressure": 1014.2,
            "rainfall": 0,
            "wind_speed": 3.4,
            "wind_direction": 180,
        }
    ]


@pytest.fixture
def sample_car_data_raw() -> list[dict[str, Any]]:
    return [
        {
            "session_key": 9478,
            "meeting_key": 1229,
            "driver_number": 1,
            "date": "2024-03-02T15:04:32.000Z",
            "speed": 250,
            "rpm": 10500,
            "throttle": 100,
            "brake": 0,
            "n_gear": 7,
            "drs": 0,
        },
        {
            "session_key": 9478,
            "meeting_key": 1229,
            "driver_number": 1,
            "date": "2024-03-02T15:04:32.270Z",
            "speed": 270,
            "rpm": 11200,
            "throttle": 100,
            "brake": 0,
            "n_gear": 7,
            "drs": 1,
        },
        {
            "session_key": 9478,
            "meeting_key": 1229,
            "driver_number": 1,
            "date": "2024-03-02T15:04:32.540Z",
            "speed": 290,
            "rpm": 11800,
            "throttle": 100,
            "brake": 0,
            "n_gear": 8,
            "drs": 1,
        },
    ]
