"""Schema Pydantic para Resultado da Sessão."""

from pydantic import BaseModel, ConfigDict


class SessionResult(BaseModel):
    """Representa a posição final e estatísticas de resultado da sessão."""

    model_config = ConfigDict(extra="ignore")

    session_key: int
    driver_number: int
    meeting_key: int | None = None
    position: int | None = None
    grid_position: int | None = None
    points: float | None = None
    status: str | None = None
    duration: float | None = None

    @property
    def position_change(self) -> int | None:
        """Calcula o ganho/perda de posições em relação ao grid de largada.

        Valor positivo indica ganho de posições, negativo perda.
        """
        if self.grid_position is not None and self.position is not None:
            return self.grid_position - self.position
        return None
