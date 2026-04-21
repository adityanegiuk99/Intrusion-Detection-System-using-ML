from __future__ import annotations

import argparse
import json
import logging
from pathlib import Path
from typing import Any

import joblib
import numpy as np
import optuna
import pandas as pd
import shap
from sklearn.base import clone
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import StratifiedKFold, cross_val_score, train_test_split

from src.preprocessing.constants import TARGET_COLUMN
from src.preprocessing.dataset import load_dataset, normalize_target
from src.preprocessing.pipeline import (
    add_engineered_features,
    build_feature_pipeline,
    summarize_numeric_reference,
)
from src.training.evaluation import evaluate_predictions, save_confusion_matrix, save_model_report
from src.training.models import build_ensemble, get_candidate_models
from src.utils.config import load_config
from src.utils.logging import configure_logging

LOGGER = logging.getLogger(__name__)


class IDSTrainer:
    def __init__(self, config: dict[str, Any]) -> None:
        self.config = config
        self.random_state = config["training"]["random_state"]
        self.output_dir = Path(config["paths"]["artifacts_dir"])
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def load_training_data(self) -> tuple[pd.DataFrame, pd.Series]:
        dataset = load_dataset(self.config["paths"]["dataset"])
        dataset = normalize_target(dataset)
        dataset = dataset.drop_duplicates().reset_index(drop=True)
        features = add_engineered_features(dataset.drop(columns=[TARGET_COLUMN, "target"], errors="ignore"))
        target = dataset["target"].map({"normal": 0, "attack": 1})
        return features, target

    def optimize_model(self, model_name: str, model, x_train, y_train):
        search_space = self.config["training"]["optuna_trials"]
        cv = StratifiedKFold(n_splits=3, shuffle=True, random_state=self.random_state)

        def objective(trial: optuna.Trial) -> float:
            candidate = clone(model)
            if model_name == "random_forest":
                candidate.set_params(
                    n_estimators=trial.suggest_int("n_estimators", 150, 350),
                    max_depth=trial.suggest_int("max_depth", 8, 24),
                    min_samples_split=trial.suggest_int("min_samples_split", 2, 8),
                )
            elif model_name == "xgboost":
                candidate.set_params(
                    n_estimators=trial.suggest_int("n_estimators", 150, 350),
                    max_depth=trial.suggest_int("max_depth", 4, 10),
                    learning_rate=trial.suggest_float("learning_rate", 0.03, 0.15),
                    subsample=trial.suggest_float("subsample", 0.7, 1.0),
                    colsample_bytree=trial.suggest_float("colsample_bytree", 0.7, 1.0),
                )
            elif model_name == "lightgbm":
                candidate.set_params(
                    n_estimators=trial.suggest_int("n_estimators", 150, 350),
                    num_leaves=trial.suggest_int("num_leaves", 16, 64),
                    learning_rate=trial.suggest_float("learning_rate", 0.03, 0.15),
                    subsample=trial.suggest_float("subsample", 0.7, 1.0),
                    colsample_bytree=trial.suggest_float("colsample_bytree", 0.7, 1.0),
                )

            scores = cross_val_score(candidate, x_train, y_train, cv=cv, scoring="roc_auc", n_jobs=1)
            return float(scores.mean())

        study = optuna.create_study(direction="maximize")
        study.optimize(objective, n_trials=search_space, show_progress_bar=False)
        optimized = clone(model)
        optimized.set_params(**study.best_params)
        return optimized, study.best_value, study.best_params

    def train(self) -> dict[str, Any]:
        features, target = self.load_training_data()
        x_train, x_test, y_train, y_test = train_test_split(
            features,
            target,
            test_size=self.config["training"]["test_size"],
            stratify=target,
            random_state=self.random_state,
        )

        pipeline_artifacts = build_feature_pipeline(k_best=self.config["training"]["k_best_features"])
        x_train_transformed = pipeline_artifacts.pipeline.fit_transform(x_train, y_train)
        x_train_processed, y_train_processed = pipeline_artifacts.resampler.fit_resample(x_train_transformed, y_train)
        x_test_processed = pipeline_artifacts.pipeline.transform(x_test)

        models = get_candidate_models(self.random_state)
        comparison_rows: list[dict[str, Any]] = []
        trained_models: dict[str, Any] = {}

        for model_name, base_model in models.items():
            LOGGER.info("Optimizing model %s", model_name)
            optimized_model, cv_score, best_params = self.optimize_model(
                model_name,
                base_model,
                x_train_processed,
                y_train_processed,
            )
            optimized_model.fit(x_train_processed, y_train_processed)
            probabilities = optimized_model.predict_proba(x_test_processed)[:, 1]
            predictions = (probabilities >= self.config["training"]["decision_threshold"]).astype(int)
            metrics = evaluate_predictions(y_test, predictions, probabilities)
            comparison_rows.append(
                {
                    "model": model_name,
                    "cv_roc_auc": round(cv_score, 4),
                    "roc_auc": round(metrics["roc_auc"], 4),
                    "best_params": best_params,
                }
            )
            trained_models[model_name] = optimized_model

        ensemble = build_ensemble(trained_models)
        ensemble.fit(x_train_processed, y_train_processed)
        ensemble_probabilities = ensemble.predict_proba(x_test_processed)[:, 1]
        ensemble_predictions = (ensemble_probabilities >= self.config["training"]["decision_threshold"]).astype(int)
        ensemble_metrics = evaluate_predictions(y_test, ensemble_predictions, ensemble_probabilities)
        comparison_rows.append(
            {
                "model": "ensemble",
                "cv_roc_auc": round(float(roc_auc_score(y_test, ensemble_probabilities)), 4),
                "roc_auc": round(ensemble_metrics["roc_auc"], 4),
                "best_params": {"members": list(trained_models.keys())},
            }
        )

        explanation_sample = shap.sample(x_test_processed, min(200, len(x_test_processed)))
        explainer = shap.Explainer(ensemble.predict_proba, explanation_sample)
        shap_values = explainer(explanation_sample)
        if shap_values.values.ndim == 3:
            mean_importance = np.abs(shap_values.values[:, :, 1]).mean(axis=0).tolist()
        else:
            mean_importance = np.abs(shap_values.values).mean(axis=0).tolist()
        selected_feature_names = self._selected_feature_names(pipeline_artifacts, x_train)

        artifacts = {
            "feature_pipeline": pipeline_artifacts.pipeline,
            "model": ensemble,
            "candidate_models": trained_models,
            "threshold": self.config["training"]["decision_threshold"],
            "labels": {0: "normal", 1: "attack"},
            "selected_feature_names": selected_feature_names,
            "shap_importance": [
                {"feature": feature, "importance": round(float(score), 6)}
                for feature, score in sorted(
                    zip(selected_feature_names, mean_importance),
                    key=lambda item: item[1],
                    reverse=True,
                )[:15]
            ],
            "numeric_reference": summarize_numeric_reference(x_train, pipeline_artifacts.numeric_columns),
            "model_report": comparison_rows,
            "evaluation": ensemble_metrics,
        }

        joblib.dump(artifacts, self.output_dir / "model_bundle.joblib")
        save_confusion_matrix(ensemble_metrics["confusion_matrix"], self.output_dir / "confusion_matrix.png")
        save_model_report(comparison_rows, self.output_dir / "model_comparison.md")
        (self.output_dir / "evaluation.json").write_text(json.dumps(ensemble_metrics, indent=2), encoding="utf-8")
        return artifacts

    def _selected_feature_names(self, pipeline_artifacts, x_train: pd.DataFrame) -> list[str]:
        selector = pipeline_artifacts.pipeline.named_steps["selector"]
        feature_names = pipeline_artifacts.pipeline.named_steps["preprocessor"].get_feature_names_out()
        mask = selector.get_support()
        return [name for name, keep in zip(feature_names, mask) if keep]


def main() -> None:
    parser = argparse.ArgumentParser(description="Train the intrusion detection models")
    parser.add_argument(
        "--config",
        default="configs/default.yaml",
        help="Path to the YAML configuration file",
    )
    args = parser.parse_args()

    config = load_config(args.config)
    configure_logging(config["app"]["log_level"])
    trainer = IDSTrainer(config)
    trainer.train()
    LOGGER.info("Training completed. Artifacts written to %s", trainer.output_dir)


if __name__ == "__main__":
    main()
