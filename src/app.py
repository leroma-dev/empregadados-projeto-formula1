"""Ponto de entrada da aplicação e Dashboard Streamlit da Fórmula 1."""

import streamlit as st

from src.components.sidebar import render_sidebar
from src.models import Driver, Lap, Meeting, Session, SessionResult, Stint, Weather
from src.services.session_service import SessionService
from src.views.lap_analysis import render_lap_analysis
from src.views.session_overview import render_session_overview
from src.views.telemetry_view import render_telemetry_view

# Configuração da página
st.set_page_config(
    page_title="OpenF1 Analytics & Dashboard",
    page_icon="🏎️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Estilização visual temática de F1
st.markdown(
    """
    <style>
    .main {
        background-color: #0E1117;
    }
    .stMetric {
        background-color: #1E2129;
        padding: 12px 18px;
        border-radius: 8px;
        border-left: 4px solid #E10600;
    }
    div[data-testid="stSidebarHeader"] {
        padding-top: 1rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_resource
def get_session_service() -> SessionService:
    """Instancia o serviço de dados da OpenF1 mantendo o cliente em cache."""
    return SessionService()


@st.cache_data(ttl=3600)
def load_session_laps(session_key: int | str) -> list[Lap]:
    """Carrega dados de voltas com cache de 1 hora."""
    service = get_session_service()
    return service.get_laps(session_key=session_key)


@st.cache_data(ttl=3600)
def load_session_stints(session_key: int | str) -> list[Stint]:
    """Carrega dados de stints com cache de 1 hora."""
    service = get_session_service()
    return service.get_stints(session_key=session_key)


@st.cache_data(ttl=3600)
def load_session_results(session_key: int | str) -> list[SessionResult]:
    """Carrega classificação final com cache de 1 hora."""
    service = get_session_service()
    return service.get_results(session_key=session_key)


@st.cache_data(ttl=3600)
def load_session_weather(session_key: int | str) -> list[Weather]:
    """Carrega meteorologia da sessão com cache de 1 hora."""
    service = get_session_service()
    return service.get_weather(session_key=session_key)


def main() -> None:
    """Função principal que orquestra a aplicação Streamlit."""
    session_service = get_session_service()

    # Barra lateral de navegação e filtros
    sidebar_selection = render_sidebar(session_service)

    meeting: Meeting | None = sidebar_selection.get("meeting")
    session: Session | None = sidebar_selection.get("session")
    drivers: list[Driver] = sidebar_selection.get("drivers", [])

    if not meeting or not session:
        st.info(
            "👈 Selecione uma Temporada, Grande Prêmio e Sessão na barra lateral para começar."
        )
        return

    # Carregar dados da sessão com cache
    session_key = session.session_key
    with st.spinner("Carregando dados da sessão OpenF1..."):
        try:
            laps = load_session_laps(session_key)
            stints = load_session_stints(session_key)
            results = load_session_results(session_key)
            weather = load_session_weather(session_key)
        except Exception as exc:
            st.error(f"Erro ao carregar dados da sessão OpenF1: {exc}")
            return

    # Abas principais de navegação
    tab_overview, tab_laps, tab_telemetry = st.tabs(
        [
            "🏆 Visão Geral da Sessão",
            "⏱️ Ritmo e Voltas",
            "⚡ Telemetria Comparativa",
        ]
    )

    with tab_overview:
        render_session_overview(
            meeting=meeting,
            session=session,
            drivers=drivers,
            results=results,
            laps=laps,
            weather=weather,
        )

    with tab_laps:
        render_lap_analysis(
            drivers=drivers,
            laps=laps,
            stints=stints,
            results=results,
        )

    with tab_telemetry:
        render_telemetry_view(
            session=session,
            drivers=drivers,
            laps=laps,
            session_service=session_service,
        )


if __name__ == "__main__":
    main()
