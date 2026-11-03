"""Schema Pydantic para Stints de Pneus."""

from pydantic import BaseModel, ConfigDict


class Stint(BaseModel):
    """Representa a utilização de um jogo de pneus em um stint."""

    model_config = ConfigDict(extra="ignore")

    session_key: int
    meeting_key: int | None = None
    driver_number: int
    stint_number: int
    compound: str | None = None
    tyre_age_at_start: int | None = None
    lap_start: int | None = None
    lap_end: int | None = None

    @property
    def total_laps(self) -> int:
        """Calcula o total de voltas percorridas no stint."""
        if self.lap_start is not None and self.lap_end is not None:
            return max(0, self.lap_end - self.lap_start + 1)
        return 0
