"""Gráficos interativos Plotly para visualização de dados de Fórmula 1."""

from typing import Any

import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Paleta padrão de cores dos compostos de pneus F1
TYRE_COMPOUND_COLORS: dict[str, str] = {
    "SOFT": "#E80020",
    "MEDIUM": "#FFF200",
    "HARD": "#FFFFFF",
    "INTERMEDIATE": "#39B54A",
    "WET": "#00A0DE",
    "TEST_UNKNOWN": "#A0A0A0",
    "UNKNOWN": "#808080",
}


def create_lap_times_chart(
    laps_df: pd.DataFrame,
    driver_colors: dict[int, str] | None = None,
) -> go.Figure:
    """Gera gráfico interativo de evolução de tempos de volta por piloto."""
    fig = go.Figure()
    driver_colors = driver_colors or {}

    if laps_df.empty:
        fig.update_layout(title="Nenhum dado de voltas disponível.")
        return fig

    for driver_number, group in laps_df.groupby("driver_number"):
        color = driver_colors.get(int(driver_number), "#888888")
        clean_group = group[
            group["lap_duration"].notnull() & (group["lap_duration"] > 0)
        ]

        fig.add_trace(
            go.Scatter(
                x=clean_group["lap_number"],
                y=clean_group["lap_duration"],
                mode="lines+markers",
                name=f"Piloto #{driver_number}",
                line=dict(color=color, width=2),
                marker=dict(size=4),
                hovertemplate="Volta %{x}: %{y:.3f}s<extra>#%{text}</extra>",
                text=[str(driver_number)] * len(clean_group),
            )
        )

    fig.update_layout(
        title="Evolução dos Tempos de Volta",
        xaxis_title="Número da Volta",
        yaxis_title="Tempo de Volta (s)",
        template="plotly_dark",
        hovermode="x unified",
        margin=dict(l=40, r=40, t=50, b=40),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )
    return fig


def create_stints_timeline_chart(stints_df: pd.DataFrame) -> go.Figure:
    """Gera gráfico horizontal da estratégia de pneus ao longo das voltas."""
    fig = go.Figure()

    if stints_df.empty:
        fig.update_layout(title="Nenhum dado de stints disponível.")
        return fig

    # Ordenar por piloto e início do stint
    sorted_stints = stints_df.sort_values(
        by=["driver_number", "stint_number"]
    ).reset_index(drop=True)

    for _, row in sorted_stints.iterrows():
        compound = str(row.get("compound", "UNKNOWN")).upper()
        color = TYRE_COMPOUND_COLORS.get(compound, "#888888")
        lap_start = row.get("lap_start") or 1
        lap_end = row.get("lap_end") or lap_start
        driver_str = f"#{row['driver_number']}"

        fig.add_trace(
            go.Bar(
                name=compound,
                y=[driver_str],
                x=[lap_end - lap_start + 1],
                base=[lap_start - 1],
                orientation="h",
                marker=dict(color=color, line=dict(color="#111111", width=1)),
                hovertemplate=(
                    f"Piloto: {driver_str}<br>"
                    f"Composto: {compound}<br>"
                    f"Voltas: {lap_start} a {lap_end}<br>"
                    f"Total: {lap_end - lap_start + 1} voltas<extra></extra>"
                ),
                showlegend=False,
            )
        )

    # Legenda explicativa com as cores dos compostos
    for comp, col in TYRE_COMPOUND_COLORS.items():
        if comp in sorted_stints["compound"].str.upper().values:
            fig.add_trace(
                go.Scatter(
                    x=[None],
                    y=[None],
                    mode="markers",
                    marker=dict(size=10, color=col),
                    name=comp,
                    showlegend=True,
                )
            )

    fig.update_layout(
        title="Estratégia e Stints de Pneus",
        xaxis_title="Volta da Corrida",
        yaxis_title="Piloto",
        barmode="stack",
        template="plotly_dark",
        margin=dict(l=60, r=40, t=50, b=40),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )
    return fig


def create_telemetry_comparison_chart(
    comp_df: pd.DataFrame,
    label_a: str,
    label_b: str,
    color_a: str = "#E10600",
    color_b: str = "#1E41FF",
) -> go.Figure:
    """Gera gráficos empilhados de telemetria comparando velocidade, acelerador e freio."""
    if comp_df.empty or "distance_m" not in comp_df.columns:
        fig = go.Figure()
        fig.update_layout(title="Sem dados suficientes para comparação de telemetria.")
        return fig

    fig = make_subplots(
        rows=3,
        cols=1,
        shared_xaxes=True,
        vertical_spacing=0.06,
        subplot_titles=(
            "Velocidade (km/h) & Delta",
            "Acelerador (%)",
            "Freio (%)",
        ),
    )

    dist = comp_df["distance_m"]

    # 1. Velocidade
    fig.add_trace(
        go.Scatter(
            x=dist,
            y=comp_df[f"speed_{label_a}"],
            name=f"Velocidade {label_a}",
            line=dict(color=color_a, width=2),
        ),
        row=1,
        col=1,
    )
    fig.add_trace(
        go.Scatter(
            x=dist,
            y=comp_df[f"speed_{label_b}"],
            name=f"Velocidade {label_b}",
            line=dict(color=color_b, width=2),
        ),
        row=1,
        col=1,
    )

    # 2. Acelerador
    fig.add_trace(
        go.Scatter(
            x=dist,
            y=comp_df[f"throttle_{label_a}"],
            name=f"Acelerador {label_a}",
            line=dict(color=color_a, width=1.5),
            showlegend=False,
        ),
        row=2,
        col=1,
    )
    fig.add_trace(
        go.Scatter(
            x=dist,
            y=comp_df[f"throttle_{label_b}"],
            name=f"Acelerador {label_b}",
            line=dict(color=color_b, width=1.5),
            showlegend=False,
        ),
        row=2,
        col=1,
    )

    # 3. Freio
    fig.add_trace(
        go.Scatter(
            x=dist,
            y=comp_df[f"brake_{label_a}"],
            name=f"Freio {label_a}",
            line=dict(color=color_a, width=1.5),
            showlegend=False,
        ),
        row=3,
        col=1,
    )
    fig.add_trace(
        go.Scatter(
            x=dist,
            y=comp_df[f"brake_{label_b}"],
            name=f"Freio {label_b}",
            line=dict(color=color_b, width=1.5),
            showlegend=False,
        ),
        row=3,
        col=1,
    )

    fig.update_layout(
        template="plotly_dark",
        height=700,
        margin=dict(l=40, r=40, t=60, b=40),
        hovermode="x unified",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )
    fig.update_xaxes(title_text="Distância no Circuito (metros)", row=3, col=1)
    fig.update_yaxes(title_text="km/h", row=1, col=1)
    fig.update_yaxes(title_text="%", row=2, col=1)
    fig.update_yaxes(title_text="%", row=3, col=1)

    return fig


def create_position_changes_chart(position_data: list[dict[str, Any]]) -> go.Figure:
    """Gera gráfico de barras horizontais indicando posições ganhas ou perdidas."""
    fig = go.Figure()

    if not position_data:
        fig.update_layout(title="Nenhum dado de grid disponível.")
        return fig

    drivers = [item["driver_name"] for item in position_data]
    changes = [item["position_change"] for item in position_data]
    colors = [
        "#39B54A" if c > 0 else "#E80020" if c < 0 else "#888888" for c in changes
    ]

    fig.add_trace(
        go.Bar(
            y=drivers,
            x=changes,
            orientation="h",
            marker=dict(color=colors),
            hovertemplate="Piloto: %{y}<br>Variação: %{x} posições<extra></extra>",
        )
    )

    fig.update_layout(
        title="Ganho e Perda de Posições (Grid ➔ Chegada)",
        xaxis_title="Variação de Posições (+ ganho / - perda)",
        yaxis_title="Piloto",
        template="plotly_dark",
        yaxis=dict(autorange="reversed"),
        margin=dict(l=120, r=40, t=50, b=40),
    )
    return fig
