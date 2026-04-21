from __future__ import annotations

from pathlib import Path
from typing import Any

import json
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    roc_auc_score,
)


def evaluate_predictions(y_true, y_pred, y_prob) -> dict[str, Any]:
    matrix = confusion_matrix(y_true, y_pred).tolist()
    report = classification_report(y_true, y_pred, output_dict=True)
    roc_auc = roc_auc_score(y_true, y_prob)
    return {
        "confusion_matrix": matrix,
        "classification_report": report,
        "roc_auc": float(roc_auc),
    }


def save_confusion_matrix(matrix: list[list[int]], output_path: str | Path) -> None:
    figure, axis = plt.subplots(figsize=(5, 4))
    axis.imshow(matrix, cmap="Blues")
    axis.set_title("Confusion Matrix")
    axis.set_xlabel("Predicted")
    axis.set_ylabel("Actual")
    for i, row in enumerate(matrix):
        for j, value in enumerate(row):
            axis.text(j, i, str(value), ha="center", va="center")
    figure.tight_layout()
    figure.savefig(output_path)
    plt.close(figure)


def save_model_report(report_rows: list[dict[str, Any]], output_path: str | Path) -> None:
    df = pd.DataFrame(report_rows).sort_values("roc_auc", ascending=False)
    if str(output_path).endswith(".md"):
        lines = [
            "# Model Comparison Report",
            "",
            df.to_markdown(index=False),
            "",
        ]
        Path(output_path).write_text("\n".join(lines), encoding="utf-8")
    else:
        Path(output_path).write_text(json.dumps(report_rows, indent=2), encoding="utf-8")

