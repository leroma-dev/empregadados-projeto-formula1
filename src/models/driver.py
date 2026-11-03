"""Schema Pydantic para Piloto de F1."""

from pydantic import BaseModel, ConfigDict


class Driver(BaseModel):
    """Representa um piloto e suas informações de equipe."""

    model_config = ConfigDict(extra="ignore")

    driver_number: int
    broadcast_name: str | None = None
    full_name: str
    name_acronym: str | None = None
    team_name: str | None = None
    team_colour: str | None = None
    headshot_url: str | None = None
    country_code: str | None = None
    session_key: int | None = None
    meeting_key: int | None = None

    @property
    def hex_colour(self) -> str:
        """Retorna a cor da equipe formatada como #RRGGBB."""
        if not self.team_colour:
            return "#CCCCCC"
        color = self.team_colour.strip()
        if not color.startswith("#"):
            return f"#{color}"
        return color
