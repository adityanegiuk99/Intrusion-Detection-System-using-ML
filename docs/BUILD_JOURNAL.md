# Build Journal

This file is meant to document real engineering progress over time. It should stay honest, lightweight, and tied to actual commits.

## Current Snapshot

The repository has moved from a notebook-led prototype toward a more application-oriented structure with:

- modular training code under `src/`
- an API service under `api/`
- a dashboard under `dashboard/`
- tests, config, Docker, and CI scaffolding

## What Has Actually Been Improved So Far

- created a clearer package structure for preprocessing, training, inference, monitoring, and streaming
- added config-driven training and inference wiring
- introduced FastAPI endpoints and a Streamlit dashboard
- added initial auth, rate limiting, metrics, Docker, and test scaffolding
- improved repository-level documentation and planning artifacts

## Known Gaps

- dataset provenance and reproducibility need stronger documentation
- model artifacts are local and not versioned through a registry
- inference still contains fallback behavior that should be replaced with explicit failure handling
- testing needs stronger negative-path and integration coverage
- prediction logging is not yet persisted to a database or durable store

## Suggested Journal Entries To Add Next

Use entries like these only when the work is actually completed:

### Entry Template

```text
## YYYY-MM-DD
- what changed
- why it mattered
- how it was validated
- what remains open
```

### Good Future Examples

- replaced fallback inference with strict artifact loading and startup validation
- added Pydantic settings and environment-specific config loading
- introduced integration tests for auth, rate limiting, and batch scoring
- added dataset schema validation before training starts
- added artifact metadata with dataset hash, training config, and metric summary

