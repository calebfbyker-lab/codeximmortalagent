# ============================================================
# CODEXIMMORTAL WARLAB — FILE METADATA HEADER
# FILE: apps/api_gateway/backend/tests/test_main.py
# MODULE: API-ROUTE-TEST-HARNESS
# LAYER: DATA
# PURPOSE: Dynamic API tests for validated registry startup, schema-versioned telemetry-backed health reporting, module listing, and module detail lookup
# DEPENDS_ON: apps/api_gateway/backend/main.py, apps/api_gateway/backend/validate_ci_registry.py, apps/api_gateway/backend/ci_registry.json, apps/api_gateway/backend/startup_telemetry.py
# EXPOSES: pytest coverage for /health, /api/modules, /api/modules/{code}
# CRYPTO_PROVENANCE: n/a
# VERSION: v4
# TAG: [CODEX-TAG: CALEB-FEDOR-BYKER-KONEV-10271998-CODEXIMMORTAL]
# ============================================================

from __future__ import annotations

from pathlib import Path

from fastapi.testclient import TestClient

from main import app
from startup_telemetry import STARTUP_TELEMETRY_SCHEMA_VERSION
from validate_ci_registry import load_validated_registry


client = TestClient(app)
registry_path = Path(__file__).resolve().parent.parent / "ci_registry.json"
registry = load_validated_registry(registry_path)
expected_modules = registry.modules
expected_module_count = len(expected_modules)
expected_ci_041 = next(module for module in expected_modules if module.code == "CI-041")


def test_health_reports_telemetry_contract() -> None:
    response = client.get("/health")
    assert response.status_code == 200

    payload = response.json()
    assert payload["schema_version"] == STARTUP_TELEMETRY_SCHEMA_VERSION
    assert payload["status"] == "ok"
    assert payload["registry_path"].endswith("ci_registry.json")
    assert payload["registry_module_count"] == expected_module_count
    assert payload["validated_at"]


def test_list_modules_returns_full_registry() -> None:
    response = client.get("/api/modules")
    assert response.status_code == 200

    payload = response.json()
    assert isinstance(payload, list)
    assert len(payload) == expected_module_count
    assert payload[0]["code"] == expected_modules[0].code
    assert payload[-1]["code"] == expected_modules[-1].code


def test_get_module_returns_specific_module() -> None:
    response = client.get(f"/api/modules/{expected_ci_041.code}")
    assert response.status_code == 200

    payload = response.json()
    assert payload["code"] == expected_ci_041.code
    assert payload["name"] == expected_ci_041.name
    assert payload["agentic_function"] == expected_ci_041.agentic_function


def test_get_module_returns_404_for_missing_code() -> None:
    response = client.get("/api/modules/CI-999")
    assert response.status_code == 404
    assert response.json()["detail"] == "module not found: CI-999"