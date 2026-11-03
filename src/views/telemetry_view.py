"""Visualização e comparação curva a curva da telemetria de alta frequência."""

import streamlit as st

from src.components.charts import create_telemetry_comparison_chart
from src.models import Driver, Lap, Session
from src.services.session_service import SessionService
from src.services.stats_service import StatsService
from src.services.telemetry_service import TelemetryService


def render_telemetry_view(
    session: Session,
    drivers: list[Driver],
    laps: list[Lap],
    session_service: SessionService,
) -> None:
    """Renderiza a aba de comparação curva a curva de telemetria."""
    st.header("⚡ Telemetria Comparativa Curva a Curva")
    st.markdown(
        "Compare a velocidade, acelerador e freio entre dois pilotos ao longo de uma volta completa."
    )

    if len(drivers) < 2:
        st.warning(
            "Necessário pelo menos 2 pilotos para realizar a comparação de telemetria."
        )
        return

    driver_options = {
        f"#{d.driver_number} - {d.full_name} ({d.team_name or 'Equipe'})": d
        for d in drivers
    }
    driver_keys = list(driver_options.keys())

    col_a, col_b = st.columns(2)
    with col_a:
        driver_a_key = st.selectbox(
            "Piloto Referência (A):",
            options=driver_keys,
            index=0,
        )
        driver_a = driver_options[driver_a_key]

    with col_b:
        driver_b_key = st.selectbox(
            "Piloto Comparado (B):",
            options=driver_keys,
            index=min(1, len(driver_keys) - 1),
        )
        driver_b = driver_options[driver_b_key]

    if driver_a.driver_number == driver_b.driver_number:
        st.warning("Selecione dois pilotos diferentes para a análise comparativa.")
        return

    # Buscar melhor volta de cada piloto
    lap_a = StatsService.get_driver_fastest_lap(laps, driver_a.driver_number)
    lap_b = StatsService.get_driver_fastest_lap(laps, driver_b.driver_number)

    time_a = (
        StatsService.format_lap_time(lap_a.lap_duration) if lap_a else "Indisponível"
    )
    time_b = (
        StatsService.format_lap_time(lap_b.lap_duration) if lap_b else "Indisponível"
    )

    st.info(
        f"**Melhor Volta {driver_a.name_acronym or driver_a.full_name}:** {time_a} | "
        f"**Melhor Volta {driver_b.name_acronym or driver_b.full_name}:** {time_b}"
    )

    load_telemetry_btn = st.button("Carregar e Comparar Telemetria", type="primary")

    if load_telemetry_btn:
        with st.spinner("Extraindo e alinhando telemetria de alta frequência..."):
            try:
                # Buscar dados de telemetria
                data_a = session_service.get_car_data(
                    session_key=session.session_key,
                    driver_number=driver_a.driver_number,
                )
                data_b = session_service.get_car_data(
                    session_key=session.session_key,
                    driver_number=driver_b.driver_number,
                )

                if not data_a or not data_b:
                    st.warning(
                        "Dados de telemetria não disponíveis para um ou ambos os pilotos nesta sessão."
                    )
                    return

                label_a = driver_a.name_acronym or f"#{driver_a.driver_number}"
                label_b = driver_b.name_acronym or f"#{driver_b.driver_number}"

                comp_df = TelemetryService.compare_laps(
                    data_a=data_a,
                    data_b=data_b,
                    label_a=label_a,
                    label_b=label_b,
                )

                if comp_df.empty:
                    st.warning("Não foi possível alinhar a telemetria das duas voltas.")
                    return

                fig_telemetry = create_telemetry_comparison_chart(
                    comp_df=comp_df,
                    label_a=label_a,
                    label_b=label_b,
                    color_a=driver_a.hex_colour,
                    color_b=driver_b.hex_colour,
                )
                st.plotly_chart(fig_telemetry, use_container_width=True)

            except Exception as exc:
                st.error(f"Erro ao processar telemetria: {exc}")
