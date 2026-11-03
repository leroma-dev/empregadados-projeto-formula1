"""Schema Pydantic para Voltas e Tempos."""

from pydantic import BaseModel, ConfigDict


class Lap(BaseModel):
    """Representa uma volta completada com tempos e setores."""

    model_config = ConfigDict(extra="ignore")

    session_key: int
    meeting_key: int | None = None
    driver_number: int
    lap_number: int
    lap_duration: float | None = None
    duration_sector_1: float | None = None
    duration_sector_2: float | None = None
    duration_sector_3: float | None = None
    i1_speed: float | None = None
    i2_speed: float | None = None
    st_speed: float | None = None
    is_pit_out_lap: bool | None = None
    date_start: str | None = None
