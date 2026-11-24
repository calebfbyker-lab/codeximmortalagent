# ============================================================
# CODEXIMMORTAL WARLAB — FILE METADATA HEADER
# FILE: apps/api_gateway/backend/README.md
# MODULE: BACKEND-RUNBOOK
# LAYER: DATA
# PURPOSE: Operational runbook for installing, validating, running, and testing the backend API gateway
# DEPENDS_ON: apps/api_gateway/backend/requirements.txt, apps/api_gateway/backend/pyproject.toml, apps/api_gateway/backend/main.py, apps/api_gateway/backend/validate_ci_registry.py
# EXPOSES: operator instructions for local development and audit readiness
# CRYPTO_PROVENANCE: unsigned documentation artifact
# VERSION: v1
# TAG: [CODEX-TAG: CALEB-FEDOR-BYKER-KONEV-10271998-CODEXIMMORTAL]
# ============================================================

# CodexImmortal API Gateway Backend

This backend serves the validated CodexImmortal CI registry through a FastAPI service. Startup loads `ci_registry.json`, validates it through the live schema, and fails fast if the registry drifts from the authoritative contract.

## Repo placement

Copy the files into this repository path:

```text
apps/api_gateway/backend/