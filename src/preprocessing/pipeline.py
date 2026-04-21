from __future__ import annotations

from dataclasses import dataclass

import pandas as pd
from imblearn.over_sampling import SMOTE
from sklearn.compose import ColumnTransformer
from sklearn.feature_selection import SelectKBest, mutual_info_classif
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from src.preprocessing.constants import CATEGORICAL_COLUMNS, FEATURE_COLUMNS


def add_engineered_features(df: pd.DataFrame) -> pd.DataFrame:
    enriched = df.copy()
    enriched["byte_ratio"] = (enriched["src_bytes"] + 1.0) / (enriched["dst_bytes"] + 1.0)
    enriched["host_error_intensity"] = (
        enriched["dst_host_serror_rate"] + enriched["dst_host_srv_serror_rate"]
    ) / 2.0
    enriched["service_error_intensity"] = (
        enriched["serror_rate"] + enriched["srv_serror_rate"] + enriched["rerror_rate"] + enriched["srv_rerror_rate"]
    ) / 4.0
    enriched["login_risk"] = enriched["num_failed_logins"] + (1 - enriched["logged_in"])
    enriched["privilege_escalation_risk"] = (
        enriched["num_compromised"] + enriched["root_shell"] + enriched["su_attempted"] + enriched["num_root"]
    )
    return enriched


@dataclass
class FeaturePipelineArtifacts:
    pipeline: Pipeline
    resampler: SMOTE
    feature_columns: list[str]
    categorical_columns: list[str]
    numeric_columns: list[str]


def build_feature_pipeline(k_best: int) -> FeaturePipelineArtifacts:
    engineered_columns = FEATURE_COLUMNS + [
        "byte_ratio",
        "host_error_intensity",
        "service_error_intensity",
        "login_risk",
        "privilege_escalation_risk",
    ]
    categorical_columns = [column for column in engineered_columns if column in CATEGORICAL_COLUMNS]
    numeric_columns = [column for column in engineered_columns if column not in categorical_columns]

    numeric_transformer = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
        ]
    )
    categorical_transformer = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("onehot", OneHotEncoder(handle_unknown="ignore", sparse_output=False)),
        ]
    )

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", numeric_transformer, numeric_columns),
            ("cat", categorical_transformer, categorical_columns),
        ]
    )

    pipeline = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("selector", SelectKBest(score_func=mutual_info_classif, k=k_best)),
        ]
    )

    return FeaturePipelineArtifacts(
        pipeline=pipeline,
        resampler=SMOTE(random_state=42),
        feature_columns=engineered_columns,
        categorical_columns=categorical_columns,
        numeric_columns=numeric_columns,
    )


def prepare_inference_frame(records: list[dict]) -> pd.DataFrame:
    frame = pd.DataFrame(records)
    for column in FEATURE_COLUMNS:
        if column not in frame.columns:
            frame[column] = 0
    frame = frame[FEATURE_COLUMNS]
    return add_engineered_features(frame)


def summarize_numeric_reference(df: pd.DataFrame, numeric_columns: list[str]) -> dict[str, dict[str, float]]:
    summary: dict[str, dict[str, float]] = {}
    for column in numeric_columns:
        values = pd.to_numeric(df[column], errors="coerce").fillna(0.0)
        summary[column] = {
            "mean": float(values.mean()),
            "std": float(values.std(ddof=0) or 1.0),
        }
    return summary
