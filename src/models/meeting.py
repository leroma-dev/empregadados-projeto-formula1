"""Schema Pydantic para Grande Prêmio (Meeting)."""

from pydantic import BaseModel, ConfigDict


class Meeting(BaseModel):
    """Representa um Grande Prêmio / Evento da Fórmula 1."""

    model_config = ConfigDict(extra="ignore")

    meeting_key: int
    meeting_name: str
    meeting_official_name: str | None = None
    circuit_key: int | None = None
    circuit_short_name: str | None = None
    country_name: str | None = None
    country_code: str | None = None
    date_start: str | None = None
    gmt_offset: str | None = None
    year: int
