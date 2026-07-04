# ============================================================
# CODEXIMMORTAL WARLAB — FILE METADATA HEADER
# FILE: apps/api_gateway/backend/tests/test_startup_telemetry_json.py
# MODULE: TELEMETRY-MANIFEST-SERIALIZATION-TEST
# LAYER: DATA
# PURPOSE: Unit test for startup telemetry JSON serialization contract
# DEPENDS_ON: apps/api_gateway/backend/app_state.py, apps/api_gateway/backend/startup_telemetry.py
# EXPOSES: pytest coverage for telemetry_json
# CRYPTO_PROVENANCE: n/a
# VERSION: v1
# TAG: [CODEX-TAG: CALEB-FEDOR-BYKER-KONEV-10271998-CODEXIMMORTAL]
# ============================================================

from __future__ import annotations

import json
from pathlib import Path

from app_state import create_app_state
from startup_telemetry import STARTUP_TELEMETRY_SCHEMA_VERSION, telemetry_json
from validate_ci_registry import load_validated_registry


registry_path = Path(__file__).resolve().parent.parent / "ci_registry.json"
registry = load_validated_registry(registry_path)
state = create_app_state(registry, registry_path)


def test_telemetry_json_serializes_schema_versioned_manifest() -> None:
    payload = json.loads(telemetry_json(state))

    assert payload["schema_version"] == STARTUP_TELEMETRY_SCHEMA_VERSION
    assert payload["status"] == "ok"
    assert payload["registry_path"].endswith("ci_registry.json")
    assert payload["registry_module_count"] == len(registry.modules)
    assert payload["validated_at"]