"""Serviço de processamento e alinhamento de dados de telemetria da F1."""

from typing import Any

import numpy as np
import pandas as pd

from src.models import CarData


class TelemetryService:
    """Processa, normaliza e compara dados de telemetria curva a curva."""

    @staticmethod
    def to_dataframe(car_data: list[CarData]) -> pd.DataFrame:
        """Converte uma lista de CarData para DataFrame pandas com cálculos derivados."""
        if not car_data:
            return pd.DataFrame(
                columns=[
                    "date",
                    "driver_number",
                    "speed",
                    "rpm",
                    "throttle",
                    "brake",
                    "n_gear",
                    "drs",
                    "time_sec",
                    "distance_m",
                ]
            )

        records = [cd.model_dump() for cd in car_data]
        df = pd.DataFrame(records)

        # Tratar tipos e ordenação temporal
        df["date"] = pd.to_datetime(df["date"], format="mixed")
        df = df.sort_values(by="date").reset_index(drop=True)

        # Converter colunas numéricas
        for col in ["speed", "rpm", "throttle", "brake"]:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

        # Tempo decorrido em segundos desde o início
        t0 = df["date"].iloc[0]
        df["time_sec"] = (df["date"] - t0).dt.total_seconds()

        # Distância aproximada percorrida (integração de velocidade km/h para metros)
        dt = df["time_sec"].diff().fillna(0)
        speed_mps = df["speed"] / 3.6
        df["distance_m"] = (speed_mps * dt).cumsum()

        return df

    @classmethod
    def interpolate_to_distance(
        cls,
        df: pd.DataFrame,
        num_points: int = 500,
    ) -> pd.DataFrame:
        """Interpola as métricas de telemetria em uma grade uniforme de distância."""
        if df.empty or len(df) < 2:
            return df

        max_dist = df["distance_m"].max()
        if max_dist <= 0:
            return df

        grid_dist = np.linspace(0, max_dist, num=num_points)
        interp_data: dict[str, Any] = {"distance_m": grid_dist}

        for col in ["speed", "rpm", "throttle", "brake", "n_gear"]:
            if col in df.columns:
                interp_data[col] = np.interp(grid_dist, df["distance_m"], df[col])

        interp_df = pd.DataFrame(interp_data)
        interp_df["driver_number"] = df["driver_number"].iloc[0]
        return interp_df

    @classmethod
    def compare_laps(
        cls,
        data_a: list[CarData],
        data_b: list[CarData],
        label_a: str = "Driver A",
        label_b: str = "Driver B",
        num_points: int = 500,
    ) -> pd.DataFrame:
        """Alinha duas voltas por distância percorrida e calcula o delta de velocidade."""
        df_a = cls.to_dataframe(data_a)
        df_b = cls.to_dataframe(data_b)

        if df_a.empty or df_b.empty:
            return pd.DataFrame()

        # Normalizar distância até o comprimento mínimo entre as duas voltas
        common_distance = min(df_a["distance_m"].max(), df_b["distance_m"].max())
        if common_distance <= 0:
            return pd.DataFrame()

        grid_dist = np.linspace(0, common_distance, num=num_points)

        speed_a = np.interp(grid_dist, df_a["distance_m"], df_a["speed"])
        speed_b = np.interp(grid_dist, df_b["distance_m"], df_b["speed"])

        throttle_a = (
            np.interp(grid_dist, df_a["distance_m"], df_a["throttle"])
            if "throttle" in df_a
            else np.zeros(num_points)
        )
        throttle_b = (
            np.interp(grid_dist, df_b["distance_m"], df_b["throttle"])
            if "throttle" in df_b
            else np.zeros(num_points)
        )

        brake_a = (
            np.interp(grid_dist, df_a["distance_m"], df_a["brake"])
            if "brake" in df_a
            else np.zeros(num_points)
        )
        brake_b = (
            np.interp(grid_dist, df_b["distance_m"], df_b["brake"])
            if "brake" in df_b
            else np.zeros(num_points)
        )

        return pd.DataFrame(
            {
                "distance_m": grid_dist,
                f"speed_{label_a}": speed_a,
                f"speed_{label_b}": speed_b,
                "speed_delta": speed_a - speed_b,
                f"throttle_{label_a}": throttle_a,
                f"throttle_{label_b}": throttle_b,
                f"brake_{label_a}": brake_a,
                f"brake_{label_b}": brake_b,
            }
        )
