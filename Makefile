# ============================================================
# CODEXIMMORTAL WARLAB — FILE METADATA HEADER
# FILE: Makefile
# MODULE: ROOT-WORKSPACE
# LAYER: INFRA
# PURPOSE: Standard developer commands for install, test, lint, backend run, and full local startup
# DEPENDS_ON: pyproject.toml, apps/api_gateway/backend/main.py, scripts/dev_run_all.sh
# EXPOSES: make install, make test, make lint, make run-backend, make dev
# CRYPTO_PROVENANCE: n/a
# VERSION: v1
# TAG: [CODEX-TAG: CALEB-FEDOR-BYKER-KONEV-10271998-CODEXIMMORTAL]
# ============================================================

.PHONY: install shell test lint format run-backend dev clean validate-registry

PYTHON ?= python3
POETRY ?= poetry
BACKEND_APP ?= apps.api_gateway.backend.main:app

install:
\t$(POETRY) install

shell:
\t$(POETRY) shell

test:
\t$(POETRY) run pytest

lint:
\t$(POETRY) run ruff check libs apps tests
\t$(POETRY) run mypy libs apps

format:
\t$(POETRY) run ruff check --fix libs apps tests

run-backend:
\t$(POETRY) run uvicorn $(BACKEND_APP) --reload

dev:
\tbash scripts/dev_run_all.sh

validate-registry:
\t$(POETRY) run $(PYTHON) -c "import json; from pathlib import Path; from core.ci_registry_schema import load_registry; data = json.loads(Path('apps/api_gateway/backend/ci_registry.json').read_text()); load_registry(data); print('ci_registry.json valid')"

clean:
\tfind . -type d -name '__pycache__' -prune -exec rm -rf {} +
\tfind . -type d -name '.pytest_cache' -prune -exec rm -rf {} +
\tfind . -type d -name '.ruff_cache' -prune -exec rm -rf {} +
\tfind . -type d -name '.mypy_cache' -prune -exec rm -rf {} +
\tfind . -type f -name '.coverage*' -delete