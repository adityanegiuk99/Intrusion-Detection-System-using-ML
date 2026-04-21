# Execution Timeline

This timeline is a forward-looking engineering plan for the next three weeks. It is not a reconstruction of past commit history.

## Time Window

- Start: April 21, 2026
- End: May 11, 2026

## Week 1: Repository Credibility and Project Framing

Dates:

- April 21, 2026 to April 27, 2026

Goals:

- make the repository easier to understand
- clearly separate current production-oriented code from legacy notebook work
- improve GitHub presentation with better docs and templates

Planned deliverables:

- README cleanup and contribution framing
- architecture, roadmap, changelog, and build journal docs
- timeline doc and issue templates
- `.env.example` and config notes
- helper scripts for training, API startup, and dashboard launch
- sample API payloads for local testing and screenshots
- notebook labeling or relocation into a legacy area

Commit ideas:

- `docs: improve repository narrative and architecture documentation`
- `chore: add issue templates and project planning docs`
- `refactor: label legacy notebooks and tighten repo structure`

## Week 2: Reliability and Validation

Dates:

- April 28, 2026 to May 4, 2026

Goals:

- make training and inference behavior more explicit and trustworthy
- strengthen reproducibility and artifact traceability

Planned deliverables:

- dataset schema validation before training
- artifact metadata manifest with config, metrics, and dataset summary
- stricter startup checks for the API
- removal or gating of fallback inference behavior
- improved API and preprocessing tests

Commit ideas:

- `feat: add dataset schema validation and artifact manifest`
- `feat: enforce strict model artifact startup checks`
- `test: expand API and preprocessing coverage`

## Week 3: Observability and Product Depth

Dates:

- May 5, 2026 to May 11, 2026

Goals:

- make the system feel more like a usable platform and less like a one-shot demo

Planned deliverables:

- prediction event logging to SQLite or JSONL
- dashboard panels for alert history and drift trend
- model/version metadata exposed in API responses or a metadata endpoint
- sample payloads and operator workflow docs

Commit ideas:

- `feat: persist prediction events for audit and dashboard history`
- `feat: add drift trend and recent alerts views to dashboard`
- `docs: add API examples and operator workflow guide`

## Suggested GitHub Issues

- Add schema validation for KDD-style datasets before training
- Persist prediction events for auditability
- Remove heuristic fallback inference in non-demo mode
- Add artifact manifest with training metadata
- Add dashboard panel for recent alert history
- Add `/model_info` endpoint exposing artifact metadata

## Suggested GitHub Milestones

- `Week 1 - Repo Credibility`
- `Week 2 - Reliability`
- `Week 3 - Observability`
