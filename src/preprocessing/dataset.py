from __future__ import annotations

from pathlib import Path

import pandas as pd

from src.preprocessing.constants import FEATURE_COLUMNS, TARGET_COLUMN


def load_dataset(data_path: str | Path) -> pd.DataFrame:
    path = Path(data_path)
    if path.suffix == ".csv":
        df = pd.read_csv(path)
    elif path.suffix == ".pkl":
        df = pd.read_pickle(path)
    else:
        df = pd.read_csv(path, names=FEATURE_COLUMNS + [TARGET_COLUMN], header=None)
    return df


def normalize_target(df: pd.DataFrame) -> pd.DataFrame:
    normalized = df.copy()
    normalized[TARGET_COLUMN] = normalized[TARGET_COLUMN].astype(str).str.strip()
    normalized["target"] = normalized[TARGET_COLUMN].map(lambda value: "normal" if value == "normal." else "attack")
    return normalized

