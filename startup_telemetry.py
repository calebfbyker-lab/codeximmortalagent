# ============================================================
# CODEXIMMORTAL WARLAB — FILE METADATA HEADER
# FILE: apps/api_gateway/backend/startup_telemetry.py
# MODULE: STARTUP-TELEMETRY-MANIFEST
# LAYER: DATA
# PURPOSE: Structured startup telemetry helpers for validated CI registry bootstrap events with schema versioning
# DEPENDS_ON: apps/api_gateway/backend/app_state.py
# EXPOSES: STARTUP_TELEMETRY_SCHEMA_VERSION, StartupTelemetry, build_startup_telemetry, telemetry_json
# CRYPTO_PROVENANCE: unsigned startup telemetry utility
# VERSION: v2
# TAG: [CODEX-TAG: CALEB-FEDOR-BYKER-KONEV-10271998-CODEXIMMORTAL]
# ============================================================

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from datetime import UTC, datetime

from app_state import AppState


STARTUP_TELEMETRY_SCHEMA_VERSION = "v1"


@dataclass(slots=True)
class StartupTelemetry:
    schema_version: str
    status: str
    registry_path: str
    registry_module_count: int
    validated_at: str


def build_startup_telemetry(state: AppState, *, status: str = "ok") -> StartupTelemetry:
    return StartupTelemetry(
        schema_version=STARTUP_TELEMETRY_SCHEMA_VERSION,
        status=status,
        registry_path=str(state.registry_path),
        registry_module_count=state.registry_module_count,
        validated_at=datetime.now(UTC).isoformat(),
    )


def telemetry_json(state: AppState, *, status: str = "ok") -> str:
    telemetry = build_startup_telemetry(state, status=status)
    return json.dumps(asdict(telemetry), indent=2)