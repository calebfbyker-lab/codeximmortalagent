# ============================================================
# CODEXIMMORTAL WARLAB — FILE METADATA HEADER
# FILE: apps/api_gateway/backend/tests/test_main.py
# MODULE: API-ROUTE-TEST-HARNESS
# LAYER: DATA
# PURPOSE: API tests for validated registry startup, health reporting, module listing, and module detail lookup
# DEPENDS_ON: apps/api_gateway/backend/main.py, apps/api_gateway/backend/ci_registry.json
# EXPOSES: pytest coverage for /health, /api/modules, /api/modules/{code}
# CRYPTO_PROVENANCE: n/a
# VERSION: v1
# TAG: [CODEX-TAG: CALEB-FEDOR-BYKER-KONEV-10271998-CODEXIMMORTAL]
# ============================================================

from __future__ import annotations

from fastapi.testclient import TestClient

from main import app


client = TestClient(app)


def test_health_reports_ok_and_registry_metadata() -> None:
    response = client.get("/health")
    assert response.status_code == 200

    payload = response.json()
    assert payload["status"] == "ok"
    assert payload["registry_path"].endswith("ci_registry.json")
    assert payload["registry_module_count"] == 53


def test_list_modules_returns_full_registry() -> None:
    response = client.get("/api/modules")
    assert response.status_code == 200

    payload = response.json()
    assert isinstance(payload, list)
    assert len(payload) == 53
    assert payload[0]["code"] == "CI-001"
    assert payload[-1]["code"] == "CI-053"


def test_get_module_returns_specific_module() -> None:
    response = client.get("/api/modules/CI-041")
    assert response.status_code == 200

    payload = response.json()
    assert payload["code"] == "CI-041"
    assert payload["name"] == "THREAT-HUNT"
    assert payload["agentic_function"] == "act"


def test_get_module_returns_404_for_missing_code() -> None:
    response = client.get("/api/modules/CI-999")
    assert response.status_code == 404
    assert response.json()["detail"] == "module not found: CI-999"