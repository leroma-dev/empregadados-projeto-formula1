"""Componentes visuais de cartões de indicadores-chave de desempenho (KPIs)."""

import streamlit as st


def render_kpi_cards(
    winner_name: str | None = None,
    winner_team: str | None = None,
    fastest_lap_time: str | None = None,
    fastest_lap_driver: str | None = None,
    track_temp: float | None = None,
    air_temp: float | None = None,
    total_laps: int | None = None,
) -> None:
    """Renderiza cartões de métricas principais no topo do dashboard."""
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            label="🏆 Vencedor",
            value=winner_name or "N/D",
            delta=winner_team,
        )

    with col2:
        st.metric(
            label="⚡ Melhor Volta",
            value=fastest_lap_time or "--:--.---",
            delta=fastest_lap_driver,
        )

    with col3:
        track_str = f"{track_temp:.1f} °C" if track_temp is not None else "N/D"
        air_str = f"Ar: {air_temp:.1f} °C" if air_temp is not None else None
        st.metric(
            label="🌡️ Temperatura da Pista",
            value=track_str,
            delta=air_str,
            delta_color="off",
        )

    with col4:
        st.metric(
            label="🏁 Total de Voltas",
            value=str(total_laps) if total_laps else "N/D",
        )
