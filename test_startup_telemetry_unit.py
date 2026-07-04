# ============================================================
# CODEXIMMORTAL WARLAB — FILE METADATA HEADER
# FILE: apps/api_gateway/backend/tests/test_startup_telemetry_unit.py
# MODULE: TELEMETRY-SCHEMA-CONSTANT-EXPOSURE-TEST
# LAYER: DATA
# PURPOSE: Unit test for startup telemetry builder schema-version propagation and registry-backed fields
# DEPENDS_ON: apps/api_gateway/backend/app_state.py, apps/api_gateway/backend/startup_telemetry.py
# EXPOSES: pytest coverage for build_startup_telemetry
# CRYPTO_PROVENANCE: n/a
# VERSION: v1
# TAG: [CODEX-TAG: CALEB-FEDOR-BYKER-KONEV-10271998-CODEXIMMORTAL]
# ============================================================

from __future__ import annotations

from pathlib import Path

from app_state import create_app_state
from startup_telemetry import STARTUP_TELEMETRY_SCHEMA_VERSION, build_startup_telemetry
from validate_ci_registry import load_validated_registry


registry_path = Path(__file__).resolve().parent.parent / "ci_registry.json"
registry = load_validated_registry(registry_path)
state = create_app_state(registry, registry_path)


def test_build_startup_telemetry_emits_shared_schema_constant() -> None:
    telemetry = build_startup_telemetry(state)

    assert telemetry.schema_version == STARTUP_TELEMETRY_SCHEMA_VERSION
    assert telemetry.status == "ok"
    assert telemetry.registry_path.endswith("ci_registry.json")
    assert telemetry.registry_module_count == len(registry.modules)
    assert telemetry.validated_at