# Changelog

All notable changes to this repository should be recorded here going forward.

The intent is not to reconstruct fake history. Start documenting from the point where the project became a structured engineering effort.

## Unreleased

### Added

- modular `src/` package for preprocessing, training, inference, monitoring, and streaming
- FastAPI application with prediction, health, token, and metrics endpoints
- Streamlit dashboard for analyst-facing traffic review
- Docker and GitHub Actions scaffolding
- repository planning and architecture documentation

### Changed

- shifted the project narrative from notebook-only experimentation toward deployable application design
- improved README structure to document goals, limitations, contributions, and future direction

### Known Limitations

- artifact handling is still local-file based
- auth flow is simplified for development
- tests are still relatively shallow
- dataset support is centered on KDD-style input

