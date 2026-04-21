# Architecture

## System Overview

The repository is organized around a simple ML platform flow:

1. raw network traffic records are loaded from a KDD-style dataset
2. preprocessing and feature engineering convert those records into model-ready features
3. multiple candidate models are trained and compared
4. an ensemble model and metadata are saved as artifacts
5. the inference service loads those artifacts for API and dashboard use

## Main Components

### `src/preprocessing`

Responsibilities:

- dataset loading
- target normalization
- feature engineering
- preprocessing and feature selection pipeline creation

Current observations:

- the feature pipeline is reusable across training and inference
- dataset support is still tightly coupled to KDD-style columns

### `src/training`

Responsibilities:

- train/test split
- SMOTE resampling
- Optuna-based tuning
- model evaluation
- artifact generation

Current observations:

- this is the strongest engineering area in the repo right now
- it still needs richer artifact metadata and stronger reproducibility support

### `src/inference`

Responsibilities:

- load trained artifacts
- prepare incoming records
- produce predictions and attach monitoring metadata

Current observations:

- API and dashboard both benefit from the shared service layer
- fallback predictions make demos easier but reduce production credibility

### `src/monitoring`

Responsibilities:

- compute a simple drift score

Current observations:

- useful as a placeholder
- not sufficient yet for production monitoring or model governance

### `api`

Responsibilities:

- serve predictions over HTTP
- expose health and metrics
- enforce basic auth and rate limiting

Current observations:

- good step toward deployability
- still needs environment-aware settings, stricter auth boundaries, and better startup validation

### `dashboard`

Responsibilities:

- make model output explorable for a human reviewer
- support CSV upload and visual triage

Current observations:

- now useful for demos and portfolio presentation
- still a prototype UI rather than a multi-user analyst product

## Data Flow

```text
Raw dataset
  -> normalize labels
  -> engineered features
  -> preprocessing transformer
  -> feature selection
  -> resampling
  -> model training and comparison
  -> saved artifact bundle
  -> inference service
  -> API and dashboard
```

## Production Weak Points

If this project is evaluated as engineering work, these are the most important weak spots to address next:

1. no formal artifact metadata or versioning contract
2. no persistent store for predictions, alerts, or audit history
3. no dataset schema enforcement before training
4. no environment-specific configuration model
5. no separation between development demo auth and production auth
6. no end-to-end integration test that exercises train -> artifact -> serve

## Recommended Next Architecture Improvements

### Short Term

- add `src/settings.py` or Pydantic settings for environment-driven config
- add artifact metadata manifest alongside the model bundle
- introduce `scripts/` for repeatable local workflows
- add `data/contracts/` for feature schema definitions

### Medium Term

- persist prediction events to SQLite or PostgreSQL
- add background jobs for batch scoring and retraining
- expose model/version metadata in the API
- split dashboard-specific transformations out of the UI file

### Longer Term

- replace simulated streaming with real log ingestion
- add model registry and deployment promotion workflow
- separate the dashboard into its own frontend service
