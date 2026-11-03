"""Análise detalhada de tempos de volta, parciais de setor e estratégia de pneus."""

import pandas as pd
import streamlit as st

from src.components.charts import (
    create_lap_times_chart,
    create_stints_timeline_chart,
)
from src.models import Driver, Lap, SessionResult, Stint
from src.services.stats_service import StatsService


def render_lap_analysis(
    drivers: list[Driver],
    laps: list[Lap],
    stints: list[Stint],
    results: list[SessionResult],
) -> None:
    """Renderiza a aba de análise de tempos de volta e stints."""
    st.header("⏱️ Análise de Ritmo e Tempos de Volta")

    if not laps:
        st.warning("Nenhum dado de voltas disponível para esta sessão.")
        return

    driver_map = {d.driver_number: d for d in drivers}
    driver_colors = {d.driver_number: d.hex_colour for d in drivers}

    # 1. Melhores Setores (S1, S2, S3) e Volta Mais Rápida
    fastest_lap = StatsService.get_fastest_lap(laps)
    sectors = StatsService.get_fastest_sectors(laps)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        fl_time = (
            StatsService.format_lap_time(fastest_lap.lap_duration)
            if fastest_lap
            else "--:--.---"
        )
        fl_d = (
            driver_map.get(fastest_lap.driver_number).name_acronym
            if (fastest_lap and driver_map.get(fastest_lap.driver_number))
            else ""
        )
        st.metric("🟣 Melhor Volta Geral", fl_time, fl_d)

    with col2:
        s1_d = (
            driver_map.get(sectors["s1"]["driver_number"]).name_acronym
            if sectors["s1"]["driver_number"]
            and driver_map.get(sectors["s1"]["driver_number"])
            else ""
        )
        s1_val = (
            f"{sectors['s1']['duration']:.3f}s"
            if sectors["s1"]["duration"]
            else "--.---"
        )
        st.metric("🟣 Setor 1 Ideal", s1_val, s1_d)

    with col3:
        s2_d = (
            driver_map.get(sectors["s2"]["driver_number"]).name_acronym
            if sectors["s2"]["driver_number"]
            and driver_map.get(sectors["s2"]["driver_number"])
            else ""
        )
        s2_val = (
            f"{sectors['s2']['duration']:.3f}s"
            if sectors["s2"]["duration"]
            else "--.---"
        )
        st.metric("🟣 Setor 2 Ideal", s2_val, s2_d)

    with col4:
        s3_d = (
            driver_map.get(sectors["s3"]["driver_number"]).name_acronym
            if sectors["s3"]["driver_number"]
            and driver_map.get(sectors["s3"]["driver_number"])
            else ""
        )
        s3_val = (
            f"{sectors['s3']['duration']:.3f}s"
            if sectors["s3"]["duration"]
            else "--.---"
        )
        st.metric("🟣 Setor 3 Ideal", s3_val, s3_d)

    st.markdown("---")

    # 2. Filtro de Pilotos para o Gráfico de Evolução de Voltas
    st.subheader("📈 Comparativo de Ritmo Volta a Volta")
    available_driver_names = {
        f"#{d.driver_number} - {d.full_name}": d.driver_number for d in drivers
    }

    # Selecionar pilotos do pódio ou top 3 por padrão
    top_driver_keys = list(available_driver_names.keys())[:3]
    selected_keys = st.multiselect(
        "Selecione os pilotos para comparar no gráfico:",
        options=list(available_driver_names.keys()),
        default=top_driver_keys,
    )
    selected_driver_nums = [
        available_driver_names[key]
        for key in selected_keys
        if key in available_driver_names
    ]

    # Filtrar dados para o gráfico
    laps_data = [
        lap.model_dump()
        for lap in laps
        if not selected_driver_nums or lap.driver_number in selected_driver_nums
    ]
    df_laps = pd.DataFrame(laps_data)

    if not df_laps.empty:
        fig_laps = create_lap_times_chart(df_laps, driver_colors=driver_colors)
        st.plotly_chart(fig_laps, use_container_width=True)
    else:
        st.info("Nenhuma volta selecionada para exibição no gráfico.")

    # 3. Estratégia de Pneus e Stints
    st.markdown("---")
    st.subheader("🛞 Estratégia de Compostos de Pneus (Stints)")
    if stints:
        stints_data = [
            stint.model_dump()
            for stint in stints
            if not selected_driver_nums or stint.driver_number in selected_driver_nums
        ]
        df_stints = pd.DataFrame(stints_data)
        if not df_stints.empty:
            fig_stints = create_stints_timeline_chart(df_stints)
            st.plotly_chart(fig_stints, use_container_width=True)
        else:
            st.info("Nenhum stint encontrado para os pilotos selecionados.")
    else:
        st.info("Dados de stints de pneus não disponíveis.")

    # 4. Comparativo de Companheiros de Equipe
    st.markdown("---")
    st.subheader("👥 Duelo entre Companheiros de Equipe")
    teammate_data = StatsService.calculate_teammate_comparison(results, drivers, laps)
    if teammate_data:
        df_teammates = pd.DataFrame(teammate_data)
        df_teammates.columns = [
            "Equipe",
            "Piloto 1",
            "Pos 1",
            "Melhor Volta 1",
            "Piloto 2",
            "Pos 2",
            "Melhor Volta 2",
            "Delta Volta (s)",
        ]
        st.dataframe(df_teammates, use_container_width=True, hide_index=True)
    else:
        st.info("Dados insuficientes para confronto direto entre companheiros.")
