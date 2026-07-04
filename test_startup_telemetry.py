# ============================================================
# CODEXIMMORTAL WARLAB — FILE METADATA HEADER
# FILE: apps/api_gateway/backend/tests/test_startup_telemetry.py
# MODULE: STARTUP-TELEMETRY-TEST-COVERAGE
# LAYER: DATA
# PURPOSE: Verify startup telemetry JSON emission during FastAPI lifespan boot
# DEPENDS_ON: apps/api_gateway/backend/main.py, apps/api_gateway/backend/startup_telemetry.py, apps/api_gateway/backend/ci_registry.json
# EXPOSES: pytest coverage for boot-time telemetry manifest shape and values
# CRYPTO_PROVENANCE: n/a
# VERSION: v1
# TAG: [CODEX-TAG: CALEB-FEDOR-BYKER-KONEV-10271998-CODEXIMMORTAL]
# ============================================================

from __future__ import annotations

import json
from pathlib import Path

from fastapi.testclient import TestClient

from main import app
from validate_ci_registry import load_validated_registry


registry_path = Path(__file__).resolve().parent.parent / "ci_registry.json"
registry = load_validated_registry(registry_path)


def test_startup_emits_structured_telemetry(capsys) -> None:
    with TestClient(app) as client:
        response = client.get("/health")
        assert response.status_code == 200

    captured = capsys.readouterr()
    telemetry = json.loads(captured.out)

    assert telemetry["status"] == "ok"
    assert telemetry["registry_path"].endswith("ci_registry.json")
    assert telemetry["registry_module_count"] == len(registry.modules)
    assert telemetry["validated_at"]