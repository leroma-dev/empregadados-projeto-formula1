"""Testes unitários para os componentes visuais e gráficos Plotly em src/components."""

from unittest.mock import MagicMock, patch

import pandas as pd
import plotly.graph_objects as go

from src.components.charts import (
    create_lap_times_chart,
    create_position_changes_chart,
    create_stints_timeline_chart,
    create_telemetry_comparison_chart,
)
from src.components.kpis import render_kpi_cards


class TestCharts:
    """Testes de geração dos gráficos Plotly."""

    def test_create_lap_times_chart_empty(self) -> None:
        fig = create_lap_times_chart(pd.DataFrame())
        assert isinstance(fig, go.Figure)

    def test_create_lap_times_chart_with_data(self) -> None:
        df = pd.DataFrame(
            [
                {"driver_number": 1, "lap_number": 1, "lap_duration": 92.5},
                {"driver_number": 1, "lap_number": 2, "lap_duration": 91.8},
                {"driver_number": 16, "lap_number": 1, "lap_duration": 93.0},
            ]
        )
        fig = create_lap_times_chart(df, driver_colors={1: "#3671C6", 16: "#E80020"})
        assert isinstance(fig, go.Figure)
        assert len(fig.data) == 2

    def test_create_stints_timeline_chart_empty(self) -> None:
        fig = create_stints_timeline_chart(pd.DataFrame())
        assert isinstance(fig, go.Figure)

    def test_create_stints_timeline_chart_with_data(self) -> None:
        df = pd.DataFrame(
            [
                {
                    "driver_number": 1,
                    "stint_number": 1,
                    "compound": "SOFT",
                    "lap_start": 1,
                    "lap_end": 15,
                },
                {
                    "driver_number": 1,
                    "stint_number": 2,
                    "compound": "HARD",
                    "lap_start": 16,
                    "lap_end": 50,
                },
            ]
        )
        fig = create_stints_timeline_chart(df)
        assert isinstance(fig, go.Figure)
        assert len(fig.data) > 0

    def test_create_telemetry_comparison_chart_empty(self) -> None:
        fig = create_telemetry_comparison_chart(pd.DataFrame(), "VER", "LEC")
        assert isinstance(fig, go.Figure)

    def test_create_telemetry_comparison_chart_with_data(self) -> None:
        df = pd.DataFrame(
            {
                "distance_m": [0, 500, 1000],
                "speed_VER": [200, 250, 310],
                "speed_LEC": [195, 245, 305],
                "throttle_VER": [100, 100, 100],
                "throttle_LEC": [90, 100, 100],
                "brake_VER": [0, 0, 0],
                "brake_LEC": [0, 0, 0],
            }
        )
        fig = create_telemetry_comparison_chart(df, "VER", "LEC")
        assert isinstance(fig, go.Figure)
        assert len(fig.data) == 6

    def test_create_position_changes_chart(self) -> None:
        empty_fig = create_position_changes_chart([])
        assert isinstance(empty_fig, go.Figure)

        data = [
            {"driver_name": "Max Verstappen", "position_change": 0},
            {"driver_name": "Sergio Perez", "position_change": 3},
            {"driver_name": "Charles Leclerc", "position_change": -2},
        ]
        fig = create_position_changes_chart(data)
        assert isinstance(fig, go.Figure)
        assert len(fig.data) == 1


class TestKPIs:
    """Testes para o renderizador de cartões de KPI."""

    @patch("streamlit.metric")
    @patch("streamlit.columns")
    def test_render_kpi_cards(
        self, mock_columns: MagicMock, mock_metric: MagicMock
    ) -> None:
        c1, c2, c3, c4 = MagicMock(), MagicMock(), MagicMock(), MagicMock()
        mock_columns.return_value = (c1, c2, c3, c4)

        render_kpi_cards(
            winner_name="Max Verstappen",
            winner_team="Red Bull",
            fastest_lap_time="1:24.321",
            fastest_lap_driver="VER",
            track_temp=35.0,
            air_temp=25.0,
            total_laps=57,
        )

        mock_columns.assert_called_once_with(4)
        assert mock_metric.call_count == 4
