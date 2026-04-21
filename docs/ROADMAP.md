# Roadmap

This roadmap is intentionally scoped to changes that are realistic for a solo builder over the next few weeks.

## Near-Term Priorities

### 1. Repository Credibility

- move legacy notebooks into a clearly labeled legacy area
- add sample data contracts and environment setup scripts
- improve docs so the repo explains what is finished vs what is still experimental

### 2. Training Pipeline Reliability

- add dataset validation before training
- log dataset size, class balance, and training config into artifact metadata
- add better evaluation outputs such as precision/recall tradeoffs and threshold analysis

### 3. Inference Hardening

- remove heuristic fallback predictions in favor of explicit startup failure or demo mode
- split token issuance into a dev-only path and a more realistic auth abstraction
- add structured request and prediction logging

### 4. Testing and CI

- add unit tests for drift logic, config loading, and preprocessing edge cases
- add API integration tests for auth failure, invalid payloads, and batch requests
- add one smoke test that trains on a small fixture dataset

### 5. Data and Monitoring

- add dataset abstraction for NSL-KDD or CIC-IDS2017
- store prediction events to file or SQLite for later analysis
- surface drift history and request volume in the dashboard

## Honest 2-3 Week Commit Sequence

### Week 1

- clean repo layout and documentation
- add architecture docs and contribution framing
- add `.env.example` and config documentation
- move notebooks under `notebooks/legacy/` or document them clearly as non-production assets

### Week 2

- add data validation and artifact metadata
- improve tests around preprocessing and API behavior
- remove or explicitly gate fallback inference mode
- add sample payloads and API examples

### Week 3

- persist prediction logs to SQLite or JSONL
- add dashboard views for recent alerts and drift history
- add service startup checks and health reporting for artifact availability
- optionally add a second dataset adapter or experiment tracking integration

## Backlog

- async inference and background batch jobs
- packet capture or Zeek log ingestion
- model registry integration
- alert routing to email, Slack, or Telegram
- analyst feedback loop and retraining trigger

