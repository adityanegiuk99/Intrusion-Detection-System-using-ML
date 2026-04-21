from __future__ import annotations

import math

import pandas as pd


def compute_drift_score(frame: pd.DataFrame, numeric_reference: dict[str, dict[str, float]]) -> float:
    if frame.empty:
        return 0.0

    scores = []
    for column, stats in numeric_reference.items():
        if column not in frame.columns:
            continue
        current_mean = float(pd.to_numeric(frame[column], errors="coerce").fillna(0.0).mean())
        baseline_mean = stats["mean"]
        baseline_std = max(stats["std"], 1e-6)
        z_shift = abs(current_mean - baseline_mean) / baseline_std
        scores.append(min(z_shift / 3.0, 1.0))

    if not scores:
        return 0.0
    return round(float(sum(scores) / len(scores)), 4)


def is_drift_detected(score: float, threshold: float) -> bool:
    return bool(score >= threshold or math.isclose(score, threshold))

