# ============================================================
# CODEXIMMORTAL WARLAB — FILE METADATA HEADER
# FILE: libs/core/tests/test_action_proof.py
# MODULE: ACTION-PROOF-TESTS
# LAYER: PROOF
# PURPOSE: Expanded unit tests for action proof creation, provider-backed verification, metadata propagation, and tamper detection
# DEPENDS_ON: libs/core/action_proof.py, libs/core/pqc_arch.py, libs/core/zk_proof.py
# EXPOSES: pytest coverage for create_proof and verify_proof across provider and backend combinations
# CRYPTO_PROVENANCE: n/a
# VERSION: v2
# TAG: [CODEX-TAG: CALEB-FEDOR-BYKER-KONEV-10271998-CODEXIMMORTAL]
# ============================================================

from __future__ import annotations

import hashlib

import pytest

from core.action_proof import MockSigningProvider, create_proof, verify_proof
from core.pqc_arch import generate_keypair
from core.zk_proof import MockZkBackend


@pytest.fixture
def signer():
    return generate_keypair("ML-DSA", classification="TS_SCI", ttl_days=14)


@pytest.fixture
def payload() -> dict:
    return {
        "mission": "hunt",
        "target": "CI-041",
        "confidence": 0.98,
        "decision": "promote",
    }


class AlternateSigningProvider(MockSigningProvider):
    name = "alternate"

    def sign(self, payload_hash: str, signer) -> str:
        return hashlib.sha3_256(f"alternate:{signer.key_id}:{payload_hash}".encode()).hexdigest()

    def verify(self, payload_hash: str, signature: str, signer_key_id: str) -> bool:
        expected = hashlib.sha3_256(f"alternate:{signer_key_id}:{payload_hash}".encode()).hexdigest()
        return signature == expected


class AlternateZkBackend(MockZkBackend):
    name = "alternate-zk"


def test_create_proof_returns_action_proof_with_expected_fields(signer, payload: dict) -> None:
    provider = MockSigningProvider()
    proof = create_proof(
        action_id="act-001",
        action_type="threat_hunt",
        actor_id="executor-node-1",
        payload=payload,
        signer=signer,
        signing_provider=provider,
    )

    assert proof.action_id == "act-001"
    assert proof.action_type == "threat_hunt"
    assert proof.actor_id == "executor-node-1"
    assert proof.signer_key_id == signer.key_id
    assert proof.signing_provider == "mock"
    assert proof.zk_proof.proof_id.startswith("zk-")


def test_verify_proof_accepts_valid_payload_and_provider(signer, payload: dict) -> None:
    provider = MockSigningProvider()
    proof = create_proof(
        action_id="act-002",
        action_type="module_promotion",
        actor_id="strategist-prime",
        payload=payload,
        signer=signer,
        signing_provider=provider,
    )

    assert verify_proof(
        proof,
        payload,
        expected_actor_id="strategist-prime",
        expected_action_type="module_promotion",
        signing_provider=provider,
    )


def test_verify_proof_rejects_tampered_payload(signer, payload: dict) -> None:
    provider = MockSigningProvider()
    proof = create_proof(
        action_id="act-003",
        action_type="module_promotion",
        actor_id="strategist-prime",
        payload=payload,
        signer=signer,
        signing_provider=provider,
    )

    tampered_payload = dict(payload)
    tampered_payload["confidence"] = 0.41

    assert not verify_proof(
        proof,
        tampered_payload,
        expected_actor_id="strategist-prime",
        expected_action_type="module_promotion",
        signing_provider=provider,
    )


def test_verify_proof_rejects_wrong_actor_id(signer, payload: dict) -> None:
    provider = MockSigningProvider()
    proof = create_proof(
        action_id="act-004",
        action_type="threat_hunt",
        actor_id="executor-node-1",
        payload=payload,
        signer=signer,
        signing_provider=provider,
    )

    assert not verify_proof(
        proof,
        payload,
        expected_actor_id="executor-node-2",
        expected_action_type="threat_hunt",
        signing_provider=provider,
    )


def test_verify_proof_rejects_wrong_action_type(signer, payload: dict) -> None:
    provider = MockSigningProvider()
    proof = create_proof(
        action_id="act-005",
        action_type="threat_hunt",
        actor_id="executor-node-1",
        payload=payload,
        signer=signer,
        signing_provider=provider,
    )

    assert not verify_proof(
        proof,
        payload,
        expected_actor_id="executor-node-1",
        expected_action_type="memory_promotion",
        signing_provider=provider,
    )


def test_verify_proof_rejects_signature_tampering(signer, payload: dict) -> None:
    provider = MockSigningProvider()
    proof = create_proof(
        action_id="act-006",
        action_type="threat_hunt",
        actor_id="executor-node-1",
        payload=payload,
        signer=signer,
        signing_provider=provider,
    )
    tampered = proof.model_copy(update={"signature": "deadbeef"})

    assert not verify_proof(
        tampered,
        payload,
        expected_actor_id="executor-node-1",
        expected_action_type="threat_hunt",
        signing_provider=provider,
    )


def test_verify_proof_rejects_provider_mismatch(signer, payload: dict) -> None:
    proof = create_proof(
        action_id="act-007",
        action_type="threat_hunt",
        actor_id="executor-node-1",
        payload=payload,
        signer=signer,
    )

    assert not verify_proof(
        proof,
        payload,
        expected_actor_id="executor-node-1",
        expected_action_type="threat_hunt",
        signing_provider=AlternateSigningProvider(),
    )


def test_custom_signing_provider_round_trip_succeeds(signer, payload: dict) -> None:
    provider = AlternateSigningProvider()
    proof = create_proof(
        action_id="act-008",
        action_type="threat_hunt",
        actor_id="executor-node-9",
        payload=payload,
        signer=signer,
        signing_provider=provider,
    )

    assert proof.signing_provider == "alternate"
    assert verify_proof(
        proof,
        payload,
        expected_actor_id="executor-node-9",
        expected_action_type="threat_hunt",
        signing_provider=provider,
    )


def test_metadata_propagates_into_action_proof_and_zk_proof(signer, payload: dict) -> None:
    provider = MockSigningProvider()
    metadata = {"mission_id": "mission-77", "priority": "critical"}
    proof = create_proof(
        action_id="act-009",
        action_type="threat_hunt",
        actor_id="executor-node-3",
        payload=payload,
        signer=signer,
        signing_provider=provider,
        metadata=metadata,
    )

    assert proof.metadata == metadata
    assert proof.zk_proof.metadata["mission_id"] == "mission-77"
    assert proof.zk_proof.metadata["priority"] == "critical"
    assert proof.zk_proof.metadata["proof_kind"] == "action"
    assert proof.zk_proof.metadata["signing_provider"] == "mock"


def test_custom_zk_backend_round_trip_succeeds(signer, payload: dict) -> None:
    provider = MockSigningProvider()
    zk_backend = AlternateZkBackend()
    proof = create_proof(
        action_id="act-010",
        action_type="threat_hunt",
        actor_id="executor-node-4",
        payload=payload,
        signer=signer,
        signing_provider=provider,
        zk_backend=zk_backend,
    )

    assert proof.zk_proof.backend_name == "alternate-zk"
    assert verify_proof(
        proof,
        payload,
        expected_actor_id="executor-node-4",
        expected_action_type="threat_hunt",
        signing_provider=provider,
        zk_backend=zk_backend,
    )


def test_verify_proof_rejects_zk_backend_mismatch(signer, payload: dict) -> None:
    provider = MockSigningProvider()
    proof = create_proof(
        action_id="act-011",
        action_type="threat_hunt",
        actor_id="executor-node-5",
        payload=payload,
        signer=signer,
        signing_provider=provider,
        zk_backend=AlternateZkBackend(),
    )

    assert not verify_proof(
        proof,
        payload,
        expected_actor_id="executor-node-5",
        expected_action_type="threat_hunt",
        signing_provider=provider,
        zk_backend=MockZkBackend(),
    )