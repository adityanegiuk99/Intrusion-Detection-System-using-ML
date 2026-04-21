from __future__ import annotations

import argparse
import json
import logging
import time
from pathlib import Path

from src.inference.service import IDSInferenceService
from src.preprocessing.dataset import load_dataset, normalize_target
from src.utils.config import load_config
from src.utils.logging import configure_logging

LOGGER = logging.getLogger(__name__)


def run_stream(config_path: str) -> None:
    config = load_config(config_path)
    configure_logging(config["app"]["log_level"])
    dataset = normalize_target(load_dataset(config["paths"]["dataset"]))
    service = IDSInferenceService(
        artifact_path=Path(config["paths"]["artifacts_dir"]) / "model_bundle.joblib",
        drift_threshold=config["monitoring"]["drift_threshold"],
    )

    interval = config["streaming"]["poll_interval_seconds"]
    sample_size = config["streaming"]["sample_size"]
    payload_records = dataset.drop(columns=["intrusion_type", "target"], errors="ignore").head(sample_size).to_dict("records")

    for record in payload_records:
        prediction = service.predict_records([record])[0]
        LOGGER.info("stream_event=%s", json.dumps({"record": record, "prediction": prediction}))
        time.sleep(interval)


def main() -> None:
    parser = argparse.ArgumentParser(description="Simulate real-time intrusion detection streaming")
    parser.add_argument("--config", default="configs/default.yaml")
    args = parser.parse_args()
    run_stream(args.config)


if __name__ == "__main__":
    main()

