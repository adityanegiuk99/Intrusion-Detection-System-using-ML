from __future__ import annotations

from typing import Any

from lightgbm import LGBMClassifier
from sklearn.ensemble import RandomForestClassifier, VotingClassifier
from xgboost import XGBClassifier


def get_candidate_models(random_state: int) -> dict[str, Any]:
    return {
        "random_forest": RandomForestClassifier(
            n_estimators=250,
            max_depth=18,
            min_samples_split=4,
            class_weight="balanced_subsample",
            random_state=random_state,
            n_jobs=-1,
        ),
        "xgboost": XGBClassifier(
            n_estimators=250,
            max_depth=8,
            learning_rate=0.08,
            subsample=0.9,
            colsample_bytree=0.9,
            eval_metric="logloss",
            random_state=random_state,
            n_jobs=-1,
        ),
        "lightgbm": LGBMClassifier(
            n_estimators=250,
            learning_rate=0.05,
            num_leaves=31,
            subsample=0.9,
            colsample_bytree=0.9,
            class_weight="balanced",
            random_state=random_state,
            n_jobs=-1,
            verbosity=-1,
        ),
    }


def build_ensemble(models: dict[str, Any]) -> VotingClassifier:
    estimators = [(name, model) for name, model in models.items()]
    return VotingClassifier(estimators=estimators, voting="soft")

