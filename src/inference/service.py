from __future__ import annotations

from pathlib import Path
from typing import Any

import joblib

from src.monitoring.drift import compute_drift_score, is_drift_detected
from src.preprocessing.pipeline import prepare_inference_frame


class IDSInferenceService:
    def __init__(self, artifact_path: str | Path, drift_threshold: float) -> None:
        path = Path(artifact_path)
        self.artifacts: dict[str, Any] | None = joblib.load(path) if path.exists() else None
        self.drift_threshold = drift_threshold

    def predict_records(self, records: list[dict]) -> list[dict[str, Any]]:
        frame = prepare_inference_frame(records)
        if self.artifacts is None:
            return self._fallback_predictions(frame)

        transformed = self.artifacts["feature_pipeline"].transform(frame)
        probabilities = self.artifacts["model"].predict_proba(transformed)[:, 1]
        threshold = self.artifacts["threshold"]
        drift_score = compute_drift_score(frame, self.artifacts["numeric_reference"])
        drift_detected = is_drift_detected(drift_score, self.drift_threshold)

        top_features = self.artifacts["shap_importance"][:5]
        outputs = []
        for probability in probabilities:
            label_id = int(probability >= threshold)
            outputs.append(
                {
                    "prediction": self.artifacts["labels"][label_id],
                    "label_id": label_id,
                    "probability": round(float(probability), 6),
                    "drift_score": drift_score,
                    "drift_detected": drift_detected,
                    "top_features": top_features,
                }
            )
        return outputs

    def _fallback_predictions(self, frame):
        outputs = []
        for _, row in frame.iterrows():
            heuristic_score = min(
                max(
                    (
                        float(row["serror_rate"])
                        + float(row["srv_serror_rate"])
                        + float(row["dst_host_serror_rate"])
                        + float(row["privilege_escalation_risk"]) / 10.0
                    )
                    / 4.0,
                    0.0,
                ),
                1.0,
            )
            label_id = int(heuristic_score >= 0.5)
            outputs.append(
                {
                    "prediction": "attack" if label_id else "normal",
                    "label_id": label_id,
                    "probability": round(float(heuristic_score), 6),
                    "drift_score": 0.0,
                    "drift_detected": False,
                    "top_features": [],
                }
            )
        return outputs
