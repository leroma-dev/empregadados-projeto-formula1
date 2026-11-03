"""Schema Pydantic para Condições Climáticas (Weather)."""

from pydantic import BaseModel, ConfigDict


class Weather(BaseModel):
    """Representa dados meteorológicos durante a sessão."""

    model_config = ConfigDict(extra="ignore")

    session_key: int
    date: str | None = None
    air_temperature: float | None = None
    track_temperature: float | None = None
    humidity: float | None = None
    pressure: float | None = None
    rainfall: int | float | bool | None = None
    wind_speed: float | None = None
    wind_direction: int | float | None = None
