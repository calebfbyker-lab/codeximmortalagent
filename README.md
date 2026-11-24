<!--
CODEXIMMORTAL — FILE METADATA
FILE: README.md
MODULE: ROOT-WORKSPACE
LAYER: DOCS
PURPOSE: Public overview, implemented interface summary, and evaluation boundaries
DEPENDS_ON: AGENTS.md, CODEXIMMORTAL.md, pyproject.toml, main.py
EXPOSES: project positioning, source navigation, API overview, and maturity limits
CRYPTO_PROVENANCE: unsigned documentation artifact; no attestation implied
VERSION: v2
TAG: [CODEX-TAG: CALEB-FEDOR-BYKER-KONEV-10271998-CODEXIMMORTAL]
-->

# CodexImmortal Agent

Governed AI engineering research with explicit contracts, inspectable interfaces, and evidence-first development.

CodexImmortal Agent explores the foundations needed to make agent-based systems easier to inspect, constrain, and evaluate. The repository includes Python registry tooling and a FastAPI entry point for exposing capability records and startup telemetry.

The broader CodexImmortal research program investigates agent governance, defensive security, provenance, and post-quantum-aware architecture. Those research directions are not a claim that every capability is implemented, integrated, or production-ready in this repository.

## Project status

Research and development. UNCERTIFIED.

This repository is being modernized to provide a consistent project structure, reproducible local setup, and a documented evaluation workflow.

Source code, tests, architecture documents, and registry entries represent different kinds of evidence:

- Source code shows an implementation, not necessarily a working integration.
- Test files show intended checks, not evidence that those checks have passed.
- Registry entries describe capabilities; they do not establish operational readiness.
- Architecture documents describe design intent unless linked to validation evidence.

Do not use this repository as an unattended production security control.

## Purpose

Agent-based software needs more than model output. Reviewers and operators need to understand:

- Which capabilities are declared.
- Which contracts govern their representation.
- What application state is exposed.
- Which behavior has been tested.
- Where human review and operational boundaries apply.

This project develops inspectable building blocks for those questions.

## Implemented API surface

The root `main.py` defines the following read-only routes:

| Method | Route | Source-defined behavior |
| --- | --- | --- |
| GET | `/health` | Returns startup telemetry derived from application state |
| GET | `/api/modules` | Returns the loaded registry's module records |
| GET | `/api/modules/{code}` | Returns a matching module record or HTTP 404 |

The application lifespan function invokes registry bootstrap and emits startup telemetry.

These descriptions are based on source inspection. Successful startup, response correctness, deployment configuration, and security properties must be verified in the intended environment.

## Source navigation

Start with these root-level files:

| File | Purpose |
| --- | --- |
| `main.py` | FastAPI application and registry routes |
| `app_state.py` | Application-state and registry-bootstrap implementation |
| `startup_telemetry.py` | Startup telemetry implementation |
| `ci_registry.json` | Repository registry data |
| `ci_registry_schema.py` | Registry schema source |
| `pyproject.toml` | Python package and tooling configuration |
| `AGENTS.md` | Contributor and coding-agent constraints |
| `CODEXIMMORTAL.md` | Repository doctrine and research context |
| `LICENSE` | License terms |

The current layout is undergoing review. File location alone does not establish that a module is correctly packaged, imported, or integrated.

## Local development

The package manifest declares Python 3.11 or newer and dependencies including FastAPI, Uvicorn, and Pydantic.

Installation and test commands are pending clean-environment verification. Packaging, import resolution, and test discovery must be aligned before this README presents a supported quick start.

A verified developer workflow should document:

1. The exact source revision and supported environment.
2. Virtual environment creation and dependency installation.
3. Registry validation.
4. Local API startup.
5. Expected responses for the documented endpoints.
6. Test execution and observed results.
7. Known limitations and cleanup.

Do not execute unfamiliar bootstrap or deployment scripts without reviewing them.

## Research scope

The wider research architecture includes:

- Governed agent orchestration.
- Defensive security workflows.
- Post-quantum cryptography research.
- Evidence and provenance mechanisms.
- Persistent state and memory governance.

Treat these as research areas unless a specific implementation includes reproducible tests and clearly documented integration evidence.

No claim is made here of certified cryptography, complete autonomous defense, production-grade distributed consensus, or deployed blockchain attestation.

## Security and operational boundaries

Use synthetic or explicitly authorized data during evaluation.

Do not commit credentials, private keys, customer information, classified material, or other restricted data.

Public API exposure, privileged integrations, production deployment, and high-consequence workflows require separate security review and approval.

This repository does not establish government endorsement, procurement status, or authorization to operate.

## Contributing

Read `AGENTS.md` before proposing changes.

Keep contributions small, reviewable, and supported by evidence. Include:

- The problem and intended behavior.
- Relevant source paths.
- Compatibility and security considerations.
- Tests added or changed.
- Commands executed and actual results.
- Known limitations and rollback considerations.

Do not change registry identities, doctrine, security boundaries, or privileged execution behavior as an incidental part of documentation cleanup.

## Relationship to commercial products

CodexImmortal Agent is a research repository. It is not a commercial payment, customer-data, or contract-execution system.

Any reuse in commercial products requires separate integration review, appropriate data isolation, and product-specific validation.

## License

See [LICENSE](LICENSE) for the applicable terms.

## Maintainer

Maintained by Caleb Byker under the CodexImmortal project.
