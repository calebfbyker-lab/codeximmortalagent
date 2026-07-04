# ============================================================
# CODEXIMMORTAL WARLAB — FILE METADATA HEADER
# FILE: libs/core/tests/test_ci_registry_schema.py
# MODULE: CI-REGISTRY-SCHEMA-TESTS
# LAYER: PQC-SPINE
# PURPOSE: Expanded unit tests for CI registry schema validation, normalization, and helper accessors
# DEPENDS_ON: libs/core/ci_registry_schema.py
# EXPOSES: pytest coverage for load_registry, find_by_code, filter_by_phase, filter_by_function, enum and tag validation
# CRYPTO_PROVENANCE: n/a
# VERSION: v2
# TAG: [CODEX-TAG: CALEB-FEDOR-BYKER-KONEV-10271998-CODEXIMMORTAL]
# ============================================================

from __future__ import annotations

import pytest
from pydantic import ValidationError

from core.ci_registry_schema import (
    CiRegistry,
    filter_by_function,
    filter_by_phase,
    find_by_code,
    load_registry,
)


@pytest.fixture
def sample_registry_data() -> list[dict]:
    return [
        {
            "code": "CI-001",
            "name": "PQC-ARCH",
            "description": "PQC architecture and HNDL exposure mapping.",
            "layer": "PQC-SPINE",
            "evolution_stage": "core",
            "agentic_function": "crypto",
            "security_class": "TS_SCI",
            "dependencies": [],
            "fractal_genetic_requirements": {
                "signing": "ML-DSA",
                "root_level": "agent",
                "merkle_required": True,
                "zk_required": True,
            },
            "rmpc_role": "state",
            "tags": ["pqc", "keys", "hndl"],
        },
        {
            "code": "CI-019",
            "name": "OSINT-FUSION",
            "description": "IOC fusion across multiple intelligence sources.",
            "layer": "OSINT",
            "evolution_stage": "operational",
            "agentic_function": "sense",
            "security_class": "SECRET",
            "dependencies": ["CI-001"],
            "fractal_genetic_requirements": {
                "signing": "ML-DSA",
                "root_level": "agent",
                "merkle_required": True,
                "zk_required": False,
            },
            "rmpc_role": "state",
            "tags": ["osint", "ioc", "fusion"],
        },
        {
            "code": "CI-053",
            "name": "ORGANIZATIONAL-RMPC-FRACTAL",
            "description": "RMPC-governed cloning with fractal cryptographic control.",
            "layer": "ORCHESTRATOR",
            "evolution_stage": "meta",
            "agentic_function": "control",
            "security_class": "SECRET",
            "dependencies": ["CI-019", "CI-001"],
            "fractal_genetic_requirements": {
                "signing": "ML-DSA",
                "root_level": "epoch",
                "merkle_required": True,
                "zk_required": True,
            },
            "rmpc_role": "control",
            "tags": ["rmpc", "swarm", "fractal"],
        },
    ]


def test_load_registry_returns_typed_registry(sample_registry_data: list[dict]) -> None:
    registry = load_registry(sample_registry_data)
    assert isinstance(registry, CiRegistry)
    assert len(registry.modules) == 3
    assert registry.modules[0].code == "CI-001"


def test_find_by_code_returns_matching_module(sample_registry_data: list[dict]) -> None:
    registry = load_registry(sample_registry_data)
    module = find_by_code(registry, "CI-019")
    assert module is not None
    assert module.name == "OSINT-FUSION"


def test_find_by_code_returns_none_for_missing_module(sample_registry_data: list[dict]) -> None:
    registry = load_registry(sample_registry_data)
    assert find_by_code(registry, "CI-404") is None


def test_filter_by_phase_returns_only_matching_modules(sample_registry_data: list[dict]) -> None:
    registry = load_registry(sample_registry_data)
    modules = filter_by_phase(registry, "meta")
    assert len(modules) == 1
    assert modules[0].code == "CI-053"


def test_filter_by_phase_returns_empty_list_when_no_match(sample_registry_data: list[dict]) -> None:
    registry = load_registry(sample_registry_data)
    modules = filter_by_phase(registry, "evolution")
    assert modules == []


def test_filter_by_function_returns_only_matching_modules(sample_registry_data: list[dict]) -> None:
    registry = load_registry(sample_registry_data)
    modules = filter_by_function(registry, "crypto")
    assert len(modules) == 1
    assert modules[0].code == "CI-001"


def test_filter_by_function_returns_empty_list_when_no_match(sample_registry_data: list[dict]) -> None:
    registry = load_registry(sample_registry_data)
    modules = filter_by_function(registry, "decide")
    assert modules == []


def test_load_registry_rejects_duplicate_module_codes(sample_registry_data: list[dict]) -> None:
    data = sample_registry_data + [dict(sample_registry_data[0])]
    with pytest.raises(ValidationError):
        load_registry(data)


def test_load_registry_rejects_unresolved_dependencies(sample_registry_data: list[dict]) -> None:
    broken = [dict(item) for item in sample_registry_data]
    broken[1]["dependencies"] = ["CI-999"]
    with pytest.raises(ValidationError):
        load_registry(broken)


def test_load_registry_rejects_self_dependency(sample_registry_data: list[dict]) -> None:
    broken = [dict(item) for item in sample_registry_data]
    broken[0]["dependencies"] = ["CI-001"]
    with pytest.raises(ValidationError):
        load_registry(broken)


def test_load_registry_rejects_malformed_ci_code(sample_registry_data: list[dict]) -> None:
    broken = [dict(item) for item in sample_registry_data]
    broken[0]["code"] = "CI-1"
    with pytest.raises(ValidationError):
        load_registry(broken)


def test_load_registry_rejects_invalid_evolution_stage(sample_registry_data: list[dict]) -> None:
    broken = [dict(item) for item in sample_registry_data]
    broken[0]["evolution_stage"] = "prototype"
    with pytest.raises(ValidationError):
        load_registry(broken)


def test_load_registry_rejects_invalid_agentic_function(sample_registry_data: list[dict]) -> None:
    broken = [dict(item) for item in sample_registry_data]
    broken[1]["agentic_function"] = "predict"
    with pytest.raises(ValidationError):
        load_registry(broken)


def test_load_registry_normalizes_tags_to_lowercase(sample_registry_data: list[dict]) -> None:
    changed = [dict(item) for item in sample_registry_data]
    changed[0]["tags"] = ["PQC", "Key Rotation", "HNDL"]
    registry = load_registry(changed)
    assert registry.modules[0].tags == ["pqc", "key-rotation", "hndl"]


def test_load_registry_rejects_duplicate_tags_after_normalization(sample_registry_data: list[dict]) -> None:
    broken = [dict(item) for item in sample_registry_data]
    broken[0]["tags"] = ["PQC", "pqc", "Pqc"]
    with pytest.raises(ValidationError):
        load_registry(broken)