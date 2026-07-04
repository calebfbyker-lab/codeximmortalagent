# ============================================================
# CODEXIMMORTAL WARLAB — FILE METADATA HEADER
# FILE: apps/api_gateway/backend/app_state.py
# MODULE: BACKEND-STARTUP-REGISTRY-GATE
# LAYER: DATA
# PURPOSE: Startup gate and application state helpers for validated CI registry loading
# DEPENDS_ON: apps/api_gateway/backend/validate_ci_registry.py
# EXPOSES: AppState, create_app_state, bootstrap_registry_state
# CRYPTO_PROVENANCE: unsigned startup state utility
# VERSION: v1
# TAG: [CODEX-TAG: CALEB-FEDOR-BYKER-KONEV-10271998-CODEXIMMORTAL]
# ============================================================

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from core.ci_registry_schema import CiRegistry

from validate_ci_registry import load_validated_registry


@dataclass(slots=True)
class AppState:
    registry: CiRegistry
    registry_path: Path
    registry_module_count: int


def create_app_state(registry: CiRegistry, registry_path: str | Path) -> AppState:
    path = Path(registry_path)
    return AppState(
        registry=registry,
        registry_path=path,
        registry_module_count=len(registry.modules),
    )


def bootstrap_registry_state(registry_path: str | Path) -> AppState:
    path = Path(registry_path)
    registry = load_validated_registry(path)
    return create_app_state(registry, path)