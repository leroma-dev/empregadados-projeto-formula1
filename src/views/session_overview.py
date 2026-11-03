"""Visão geral da sessão: classificação, KPIs e condições de pista."""

from typing import Any

import pandas as pd
import streamlit as st

from src.components.charts import create_position_changes_chart
from src.components.kpis import render_kpi_cards
from src.models import Driver, Lap, Meeting, Session, SessionResult, Weather
from src.services.stats_service import StatsService


def render_session_overview(
    meeting: Meeting,
    session: Session,
    drivers: list[Driver],
    results: list[SessionResult],
    laps: list[Lap],
    weather: list[Weather],
) -> None:
    """Renderiza a aba de visão geral e resultados da sessão."""
    st.header(f"🏁 {meeting.meeting_name} — {session.session_name}")

    # 1. Identificar dados para os KPIs
    driver_map = {d.driver_number: d for d in drivers}
    winner = None
    if results:
        p1 = results[0]
        winner = driver_map.get(p1.driver_number)

    fastest_lap = StatsService.get_fastest_lap(laps)
    fl_driver = driver_map.get(fastest_lap.driver_number) if fastest_lap else None
    fl_time_str = (
        StatsService.format_lap_time(fastest_lap.lap_duration) if fastest_lap else None
    )
    fl_driver_str = fl_driver.full_name if fl_driver else None

    latest_weather = weather[-1] if weather else None
    track_temp = latest_weather.track_temperature if latest_weather else None
    air_temp = latest_weather.air_temperature if latest_weather else None

    total_laps = max((lap.lap_number for lap in laps), default=0)

    # 2. Renderizar KPIs
    render_kpi_cards(
        winner_name=winner.full_name if winner else None,
        winner_team=winner.team_name if winner else None,
        fastest_lap_time=fl_time_str,
        fastest_lap_driver=fl_driver_str,
        track_temp=track_temp,
        air_temp=air_temp,
        total_laps=total_laps,
    )

    st.markdown("---")

    # 3. Tabela de Classificação Final
    st.subheader("📋 Classificação Oficial")
    if results:
        table_rows: list[dict[str, Any]] = []
        for r in results:
            d = driver_map.get(r.driver_number)
            pos_change = r.position_change
            change_str = (
                f"+{pos_change}"
                if pos_change and pos_change > 0
                else str(pos_change)
                if pos_change is not None
                else "-"
            )

            table_rows.append(
                {
                    "Posição": r.position or "DNF",
                    "Nº": r.driver_number,
                    "Piloto": d.full_name if d else f"#{r.driver_number}",
                    "Equipe": d.team_name if d else "N/A",
                    "Grid": r.grid_position or "-",
                    "Variação": change_str,
                    "Pontos": r.points or 0.0,
                    "Status": r.status or "Classificado",
                }
            )

        df_results = pd.DataFrame(table_rows)
        st.dataframe(df_results, use_container_width=True, hide_index=True)
    else:
        st.info("Classificação ainda não disponível para esta sessão.")

    # 4. Gráfico de Ganho/Perda de Posições
    st.markdown("---")
    st.subheader("📊 Variação em Relação ao Grid de Largada")
    pos_data = StatsService.calculate_position_changes(results, drivers)
    if pos_data:
        chart_fig = create_position_changes_chart(pos_data)
        st.plotly_chart(chart_fig, use_container_width=True)
    else:
        st.info("Dados de grid não disponíveis para gerar gráfico de variação.")
