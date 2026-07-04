# ============================================================
# CODEXIMMORTAL WARLAB — FILE METADATA HEADER
# FILE: apps/api_gateway/backend/validate_ci_registry.py
# MODULE: CI-REGISTRY-VALIDATION-HARNESS
# LAYER: DATA
# PURPOSE: Fail-fast validation harness for ci_registry.json using the live CI registry schema
# DEPENDS_ON: apps/api_gateway/backend/ci_registry.json, libs/core/ci_registry_schema.py
# EXPOSES: validate_registry_file, load_validated_registry
# CRYPTO_PROVENANCE: unsigned startup validation utility
# VERSION: v1
# TAG: [CODEX-TAG: CALEB-FEDOR-BYKER-KONEV-10271998-CODEXIMMORTAL]
# ============================================================

from __future__ import annotations

import json
from pathlib import Path

from core.ci_registry_schema import CiRegistry, load_registry


DEFAULT_REGISTRY_PATH = Path(__file__).with_name("ci_registry.json")


def validate_registry_file(path: str | Path = DEFAULT_REGISTRY_PATH) -> CiRegistry:
    registry_path = Path(path)
    raw = json.loads(registry_path.read_text(encoding="utf-8"))
    return load_registry(raw)


def load_validated_registry(path: str | Path = DEFAULT_REGISTRY_PATH) -> CiRegistry:
    return validate_registry_file(path)


if __name__ == "__main__":
    registry = validate_registry_file()
    print(f"validated {len(registry.modules)} modules from {DEFAULT_REGISTRY_PATH.name}")