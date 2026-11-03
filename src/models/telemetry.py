"""Schema Pydantic para Telemetria de Carro (Car Data)."""

from pydantic import BaseModel, ConfigDict


class CarData(BaseModel):
    """Representa a telemetria do carro em alta frequência."""

    model_config = ConfigDict(extra="ignore")

    driver_number: int
    date: str
    speed: int | float
    rpm: int | float | None = None
    throttle: int | float | None = None
    brake: int | float | None = None
    n_gear: int | None = None
    drs: int | None = None
    session_key: int | None = None
    meeting_key: int | None = None
