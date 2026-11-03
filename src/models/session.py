"""Schema Pydantic para Sessão de F1."""

from pydantic import BaseModel, ConfigDict


class Session(BaseModel):
    """Representa uma sessão de F1 (Treino, Classificação, Sprint ou Corrida)."""

    model_config = ConfigDict(extra="ignore")

    session_key: int
    meeting_key: int
    session_name: str
    session_type: str | None = None
    date_start: str | None = None
    date_end: str | None = None
    gmt_offset: str | None = None
    year: int | None = None
