"""Serviço de cálculos estatísticos e métricas de desempenho de Fórmula 1."""

from typing import Any

from src.models import Driver, Lap, SessionResult, Stint


class StatsService:
    """Implementa análises e cálculos estatísticos sobre os dados de F1."""

    @staticmethod
    def format_lap_time(seconds: float | None) -> str:
        """Formata duração em segundos no padrão F1 'M:SS.mmm'."""
        if seconds is None or seconds <= 0:
            return "--:--.---"
        minutes = int(seconds // 60)
        rem_seconds = seconds % 60
        return f"{minutes}:{rem_seconds:06.3f}"

    @classmethod
    def get_fastest_lap(cls, laps: list[Lap]) -> Lap | None:
        """Retorna a volta mais rápida da sessão (menor lap_duration válido)."""
        valid_laps = [
            lap
            for lap in laps
            if lap.lap_duration is not None
            and lap.lap_duration > 0
            and not lap.is_pit_out_lap
        ]
        if not valid_laps:
            return None
        return min(valid_laps, key=lambda lap: lap.lap_duration or float("inf"))

    @classmethod
    def get_driver_fastest_lap(cls, laps: list[Lap], driver_number: int) -> Lap | None:
        """Retorna a volta mais rápida de um piloto específico."""
        driver_laps = [lap for lap in laps if lap.driver_number == driver_number]
        return cls.get_fastest_lap(driver_laps)

    @classmethod
    def get_fastest_sectors(cls, laps: list[Lap]) -> dict[str, dict[str, Any]]:
        """Identifica os melhores tempos de setor (S1, S2, S3) e os respectivos pilotos."""
        best_s1: tuple[float, Lap | None] = (float("inf"), None)
        best_s2: tuple[float, Lap | None] = (float("inf"), None)
        best_s3: tuple[float, Lap | None] = (float("inf"), None)

        for lap in laps:
            if lap.duration_sector_1 and lap.duration_sector_1 < best_s1[0]:
                best_s1 = (lap.duration_sector_1, lap)
            if lap.duration_sector_2 and lap.duration_sector_2 < best_s2[0]:
                best_s2 = (lap.duration_sector_2, lap)
            if lap.duration_sector_3 and lap.duration_sector_3 < best_s3[0]:
                best_s3 = (lap.duration_sector_3, lap)

        return {
            "s1": {
                "duration": best_s1[0] if best_s1[1] else None,
                "driver_number": best_s1[1].driver_number if best_s1[1] else None,
                "lap_number": best_s1[1].lap_number if best_s1[1] else None,
            },
            "s2": {
                "duration": best_s2[0] if best_s2[1] else None,
                "driver_number": best_s2[1].driver_number if best_s2[1] else None,
                "lap_number": best_s2[1].lap_number if best_s2[1] else None,
            },
            "s3": {
                "duration": best_s3[0] if best_s3[1] else None,
                "driver_number": best_s3[1].driver_number if best_s3[1] else None,
                "lap_number": best_s3[1].lap_number if best_s3[1] else None,
            },
        }

    @classmethod
    def calculate_race_pace(
        cls,
        laps: list[Lap],
        driver_number: int,
        exclude_pit: bool = True,
    ) -> float | None:
        """Calcula a média de tempo de volta do piloto, excluindo voltas de pit e anomalias."""
        driver_laps = [lap for lap in laps if lap.driver_number == driver_number]
        valid_durations: list[float] = []

        for lap in driver_laps:
            if lap.lap_duration is None or lap.lap_duration <= 0:
                continue
            if exclude_pit and lap.is_pit_out_lap:
                continue
            valid_durations.append(lap.lap_duration)

        if not valid_durations:
            return None

        # Excluir voltas de Safety Car / anomalias (mais de 115% da mediana/mínimo)
        min_lap = min(valid_durations)
        filtered = [d for d in valid_durations if d <= min_lap * 1.15]
        if not filtered:
            filtered = valid_durations

        return sum(filtered) / len(filtered)

    @classmethod
    def calculate_stint_statistics(
        cls,
        laps: list[Lap],
        stints: list[Stint],
    ) -> list[dict[str, Any]]:
        """Calcula o ritmo médio e degradação para cada stint de pneus de cada piloto."""
        stats: list[dict[str, Any]] = []

        for stint in stints:
            stint_laps = [
                lap
                for lap in laps
                if lap.driver_number == stint.driver_number
                and stint.lap_start is not None
                and stint.lap_end is not None
                and stint.lap_start <= lap.lap_number <= stint.lap_end
                and lap.lap_duration is not None
                and lap.lap_duration > 0
                and not lap.is_pit_out_lap
            ]

            durations = [
                lap.lap_duration for lap in stint_laps if lap.lap_duration is not None
            ]
            avg_pace = sum(durations) / len(durations) if durations else None
            best_lap = min(durations) if durations else None

            stats.append(
                {
                    "driver_number": stint.driver_number,
                    "stint_number": stint.stint_number,
                    "compound": stint.compound or "UNKNOWN",
                    "tyre_age_at_start": stint.tyre_age_at_start or 0,
                    "lap_start": stint.lap_start,
                    "lap_end": stint.lap_end,
                    "total_laps": stint.total_laps,
                    "average_pace": avg_pace,
                    "best_lap": best_lap,
                }
            )

        return stats

    @classmethod
    def calculate_position_changes(
        cls,
        results: list[SessionResult],
        drivers: list[Driver],
    ) -> list[dict[str, Any]]:
        """Gera a tabela comparativa de ganho/perda de posições em relação ao grid de largada."""
        driver_map = {d.driver_number: d for d in drivers}
        changes: list[dict[str, Any]] = []

        for result in results:
            driver = driver_map.get(result.driver_number)
            name = driver.full_name if driver else f"Piloto #{result.driver_number}"
            team = driver.team_name if driver else "N/A"
            color = driver.hex_colour if driver else "#888888"

            changes.append(
                {
                    "driver_number": result.driver_number,
                    "driver_name": name,
                    "team_name": team,
                    "color": color,
                    "grid_position": result.grid_position,
                    "finish_position": result.position,
                    "position_change": result.position_change or 0,
                    "points": result.points or 0.0,
                    "status": result.status or "Finished",
                }
            )

        return sorted(
            changes,
            key=lambda item: (
                item["finish_position"] is None,
                item["finish_position"] or 999,
            ),
        )

    @classmethod
    def calculate_teammate_comparison(
        cls,
        results: list[SessionResult],
        drivers: list[Driver],
        laps: list[Lap],
    ) -> list[dict[str, Any]]:
        """Compara o desempenho entre pilotos da mesma equipe."""
        team_drivers: dict[str, list[Driver]] = {}
        for driver in drivers:
            team = driver.team_name or "Independent"
            team_drivers.setdefault(team, []).append(driver)

        results_map = {r.driver_number: r for r in results}
        comparisons: list[dict[str, Any]] = []

        for team, d_list in team_drivers.items():
            if len(d_list) < 2:
                continue

            d1, d2 = d_list[0], d_list[1]
            r1, r2 = (
                results_map.get(d1.driver_number),
                results_map.get(d2.driver_number),
            )
            fl1 = cls.get_driver_fastest_lap(laps, d1.driver_number)
            fl2 = cls.get_driver_fastest_lap(laps, d2.driver_number)

            t1 = fl1.lap_duration if fl1 else None
            t2 = fl2.lap_duration if fl2 else None
            lap_delta = (t1 - t2) if (t1 is not None and t2 is not None) else None

            comparisons.append(
                {
                    "team_name": team,
                    "driver_1": d1.name_acronym or d1.full_name,
                    "driver_1_pos": r1.position if r1 else None,
                    "driver_1_fl": cls.format_lap_time(t1),
                    "driver_2": d2.name_acronym or d2.full_name,
                    "driver_2_pos": r2.position if r2 else None,
                    "driver_2_fl": cls.format_lap_time(t2),
                    "lap_delta_seconds": lap_delta,
                }
            )

        return comparisons
