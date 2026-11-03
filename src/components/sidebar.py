"""Componente de barra lateral (Sidebar) para filtros e seleções no Streamlit."""

from typing import Any

import streamlit as st

from src.models import Driver, Meeting, Session
from src.services.session_service import SessionService


def render_sidebar(
    session_service: SessionService,
) -> dict[str, Any]:
    """Renderiza os seletores da sidebar e retorna as entidades selecionadas pelo usuário."""
    st.sidebar.image(
        "https://upload.wikimedia.org/wikipedia/commons/3/33/F1.svg",
        width=140,
    )
    st.sidebar.title("OpenF1 Analytics")
    st.sidebar.markdown("---")

    # 1. Seleção de Ano da Temporada
    year = st.sidebar.selectbox(
        "Temporada",
        options=[2024, 2023],
        index=0,
        help="A OpenF1 disponibiliza dados a partir da temporada de 2023.",
    )

    # 2. Seleção de Grande Prêmio
    meetings: list[Meeting] = []
    try:
        meetings = session_service.get_meetings(year=year)
    except Exception as exc:
        st.sidebar.error(f"Erro ao carregar GPs: {exc}")

    if not meetings:
        st.sidebar.warning("Nenhum Grande Prêmio encontrado.")
        return {"year": year, "meeting": None, "session": None, "drivers": []}

    meeting_options = {
        f"{m.meeting_name} ({m.country_name or 'GP'})": m for m in meetings
    }
    selected_meeting_name = st.sidebar.selectbox(
        "Grande Prêmio",
        options=list(meeting_options.keys()),
        index=len(meeting_options) - 1,  # Padrão para o último GP da lista
    )
    selected_meeting = meeting_options[selected_meeting_name]

    # 3. Seleção de Sessão
    sessions: list[Session] = []
    try:
        sessions = session_service.get_sessions(
            meeting_key=selected_meeting.meeting_key
        )
    except Exception as exc:
        st.sidebar.error(f"Erro ao carregar sessões: {exc}")

    if not sessions:
        st.sidebar.warning("Nenhuma sessão disponível para este GP.")
        return {
            "year": year,
            "meeting": selected_meeting,
            "session": None,
            "drivers": [],
        }

    session_options = {s.session_name: s for s in sessions}
    # Selecionar preferencialmente "Race"
    default_session_index = 0
    for idx, name in enumerate(session_options.keys()):
        if "race" in name.lower() or "corrida" in name.lower():
            default_session_index = idx
            break

    selected_session_name = st.sidebar.selectbox(
        "Sessão",
        options=list(session_options.keys()),
        index=default_session_index,
    )
    selected_session = session_options[selected_session_name]

    # 4. Lista de Pilotos da Sessão
    drivers: list[Driver] = []
    try:
        drivers = session_service.get_drivers(session_key=selected_session.session_key)
    except Exception as exc:
        st.sidebar.error(f"Erro ao carregar pilotos: {exc}")

    st.sidebar.markdown("---")
    st.sidebar.info(
        f"**Sessão Ativa:** {selected_session.session_name}\n\n"
        f"**Circuito:** {selected_meeting.circuit_short_name or selected_meeting.meeting_name}\n\n"
        f"**Pilotos Identificados:** {len(drivers)}"
    )

    return {
        "year": year,
        "meeting": selected_meeting,
        "session": selected_session,
        "drivers": drivers,
    }
