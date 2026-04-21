# Intrusion Detection Platform

An intrusion detection project that started as a notebook-based machine learning experiment and is being rebuilt into a more production-oriented platform for batch scoring, API inference, dashboard review, and operational hardening.

This repository is intentionally presented as an engineering-in-progress project rather than a finished enterprise product. The goal is to show real system design, iterative improvement, and honest productionization work on top of a classical IDS dataset.

## Project Goal

The project aims to detect malicious network traffic using machine learning and expose the model through a usable application stack:

- a reproducible training pipeline
- a FastAPI inference service
- a Streamlit analyst dashboard
- basic monitoring and drift checks
- Docker-based local deployment

The longer-term objective is to move from offline dataset classification toward a more realistic security analytics workflow with stronger validation, observability, and deployment discipline.

## What This Repository Currently Contains

- Config-driven preprocessing, feature engineering, feature selection, and SMOTE-based class balancing
- Model comparison across Random Forest, XGBoost, LightGBM, and a soft-voting ensemble
- FastAPI endpoints for health, model metadata, single prediction, batch prediction, metrics, and token generation
- A Streamlit dashboard for analyst review and batch triage
- A streaming simulator that replays records through the shared inference layer
- Basic drift scoring based on feature distribution shifts
- Docker, CI, linting, and pytest scaffolding

## Architecture

```text
Dataset / CSV stream
        |
        v
+--------------------+
| Preprocessing      |
| feature engineering|
| selection + SMOTE  |
+---------+----------+
          |
          v
+--------------------+      +---------------------+
| Training pipeline  |----->| model artifacts     |
| tuning + evaluation|      | metrics + SHAP data |
+---------+----------+      +----------+----------+
          |                            |
          |                            |
          v                            v
+--------------------+      +---------------------+
| FastAPI service    |      | Streamlit dashboard |
| auth + rate limit  |      | analyst review UI   |
| health + metrics   |      | visual triage       |
+--------------------+      +---------------------+
```

More detail: [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)

## Dataset and Source

The current implementation is built around the KDD Cup / KDD '99 style intrusion detection dataset layout used by the original notebook project.

- Expected raw file path: `data/raw/kddcup.data_10_percent_corrected`
- Original dataset source: [KDD Cup 1999 Data](http://kdd.ics.uci.edu/databases/kddcup99/kddcup99.html)
- Current framing in this repository: binary classification (`normal` vs `attack`)

Important caveat:

- KDD '99 is a useful educational benchmark, but it is not a modern production traffic source.
- A more credible next step would be to support NSL-KDD, CIC-IDS2017, Zeek logs, or NetFlow-style telemetry.

## My Actual Contributions

To keep this repository credible, this section describes the work reflected in the current codebase rather than claiming authorship over the original notebook history.

My work in this repository includes:

- restructuring the project into `src`, `api`, `dashboard`, `configs`, and `tests`
- converting the workflow from notebook-first toward reusable Python modules
- adding a training pipeline with feature engineering, SMOTE, model comparison, and Optuna-based tuning
- adding a FastAPI inference layer with JWT support, rate limiting, and Prometheus metrics
- building a Streamlit dashboard for batch review and analyst-facing visualization
- adding Docker and CI scaffolding
- improving repository documentation, roadmap visibility, and engineering planning

Work that still needs to be done:

- strengthen dataset handling and provenance
- improve test depth beyond smoke-level coverage
- replace heuristic fallback behavior with stricter service startup guarantees
- improve deployment realism and monitoring depth

## Repository Structure

```text
.
+-- api/                   # FastAPI application
+-- configs/               # YAML configuration
+-- dashboard/             # Streamlit dashboard
+-- data/                  # Dataset location and derived data
+-- docs/                  # Architecture, roadmap, journal, changelog
+-- models/                # Saved artifacts
+-- notebooks/             # Legacy exploration notebooks
+-- src/
|   +-- inference/
|   +-- monitoring/
|   +-- preprocessing/
|   +-- streaming/
|   +-- training/
|   `-- utils/
+-- tests/
+-- Dockerfile
+-- docker-compose.yml
`-- requirements.txt
```

## Cleaner Organization Recommendations

The current structure is workable, but a cleaner next iteration would be:

```text
.
+-- api/
+-- dashboard/
+-- configs/
+-- docs/
+-- scripts/
|   +-- train.ps1
|   +-- run_api.ps1
|   `-- run_dashboard.ps1
+-- src/
+-- tests/
+-- data/
|   +-- sample/
|   `-- schemas/
+-- artifacts/
`-- notebooks/
    `-- legacy/
```

Why this would help:

- `docs/` keeps project narrative and planning separate from code
- `scripts/` makes local workflows easier to discover
- `artifacts/` is a clearer home for generated model output than `models/artifacts`
- `notebooks/legacy/` makes it obvious which assets are reference material only

## Local Setup

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python -m src.training.trainer --config configs/default.yaml
uvicorn api.main:app --reload
```

Run the dashboard:

```bash
streamlit run dashboard/app.py
```

Run tests:

```bash
python -m pytest
python -m ruff check .
```

Helper scripts:

```powershell
./scripts/train.ps1
./scripts/run_api.ps1
./scripts/run_dashboard.ps1
```

Sample request bodies:

- [data/sample/predict_request.json](data/sample/predict_request.json)
- [data/sample/batch_predict_request.json](data/sample/batch_predict_request.json)

Useful API endpoints:

- `GET /health`
- `GET /model_info`
- `POST /token`
- `POST /predict`
- `POST /batch_predict`

Environment setup:

- copy `.env.example` to `.env`
- set `IDS_JWT_SECRET` before running the API outside local demo use

## Weak Spots and Honest Next Steps

These are the current weak points that matter most if this repo is meant to look serious:

1. The dataset is old and the problem framing is still mostly educational.
2. The API token flow is demo-friendly, not production-grade auth.
3. The inference service includes a heuristic fallback when model artifacts are missing.
4. Test coverage is shallow and mostly checks happy paths.
5. There is no persistent prediction store, audit log backend, or retraining workflow.
6. The legacy notebooks still exist and can blur the story of where the real application logic lives.

## Roadmap

Short-term roadmap:

- tighten repository structure and docs
- improve dataset handling and validation
- add stronger tests and failure-mode handling
- add artifact/version metadata and reproducibility docs
- improve service deployment realism

Detailed planning:

- [docs/ROADMAP.md](docs/ROADMAP.md)
- [docs/BUILD_JOURNAL.md](docs/BUILD_JOURNAL.md)
- [docs/CHANGELOG.md](docs/CHANGELOG.md)
- [docs/TIMELINE.md](docs/TIMELINE.md)

## Portfolio-Friendly Follow-Up Repositories

These are realistic spin-off repositories that are genuinely distinct:

1. `ids-model-monitoring`
   A dedicated monitoring service for drift, latency, alert rates, and model health.
2. `ids-inference-deployment`
   A deployment-focused repo with Terraform, Docker, reverse proxying, and cloud rollout.
3. `ids-data-validation`
   A pipeline for schema checks, feature contracts, and data quality monitoring.
4. `ids-experiment-tracking`
   MLflow or Weights & Biases based experiment tracking and model registry workflows.
5. `ids-frontend-console`
   A React-based SOC-style frontend replacing the Streamlit prototype.

## License

This project is released under the terms of the [LICENSE](LICENSE).
