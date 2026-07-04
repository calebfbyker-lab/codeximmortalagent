# ============================================================
# CODEXIMMORTAL WARLAB — FILE METADATA HEADER
# FILE: libs/core/action_proof.py
# MODULE: CI-050
# LAYER: PROOF
# PURPOSE: Action proof model and provider-backed proof creation/verification utilities linking signing and ZK attestation semantics
# DEPENDS_ON: libs/core/pqc_arch.py, libs/core/zk_proof.py
# EXPOSES: ActionProof, SigningProvider, MockSigningProvider, create_proof, verify_proof
# CRYPTO_PROVENANCE: unsigned development stub; interface designed for ML-DSA signing and ZK-linked action attestations
# VERSION: v2
# TAG: [CODEX-TAG: CALEB-FEDOR-BYKER-KONEV-10271998-CODEXIMMORTAL]
# ============================================================

from __future__ import annotations

import hashlib
import json
from datetime import UTC, datetime
from typing import Any, Protocol

from pydantic import BaseModel, ConfigDict, Field

from core.pqc_arch import KeyPair
from core.zk_proof import ZkCircuit, ZkProof, create_zk_proof, verify_zk_proof


class ActionProof(BaseModel):
    model_config = ConfigDict(extra="forbid")

    action_id: str
    action_type: str
    actor_id: str
    payload_hash: str
    signature: str
    signer_key_id: str
    signing_provider: str = "mock"
    zk_proof: ZkProof
    created_at: datetime
    metadata: dict[str, Any] = Field(default_factory=dict)


class SigningProvider(Protocol):
    name: str

    def sign(self, payload_hash: str, signer: KeyPair) -> str: ...

    def verify(self, payload_hash: str, signature: str, signer_key_id: str) -> bool: ...


class MockSigningProvider:
    name = "mock"

    def sign(self, payload_hash: str, signer: KeyPair) -> str:
        return hashlib.sha3_256(f"{signer.key_id}:{payload_hash}".encode()).hexdigest()

    def verify(self, payload_hash: str, signature: str, signer_key_id: str) -> bool:
        expected = hashlib.sha3_256(f"{signer_key_id}:{payload_hash}".encode()).hexdigest()
        return signature == expected


DEFAULT_SIGNING_PROVIDER: SigningProvider = MockSigningProvider()


def _stable_hash(payload: Any) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str).encode()
    return hashlib.sha3_256(encoded).hexdigest()


def create_proof(
    action_id: str,
    action_type: str,
    actor_id: str,
    payload: dict[str, Any],
    signer: KeyPair,
    *,
    metadata: dict[str, Any] | None = None,
    signing_provider: SigningProvider | None = None,
) -> ActionProof:
    now = datetime.now(UTC)
    provider = signing_provider or DEFAULT_SIGNING_PROVIDER
    payload_hash = _stable_hash(payload)
    signature = provider.sign(payload_hash, signer)
    zk_proof = create_zk_proof(
        ZkCircuit.CIRC_003_ACTION_PROOF,
        public_inputs={
            "action_id": action_id,
            "action_type": action_type,
            "actor_id": actor_id,
            "payload_hash": payload_hash,
        },
        witness={
            "signature": signature,
            "signer_key_id": signer.key_id,
            "signing_provider": provider.name,
        },
        signer=signer,
        metadata={"proof_kind": "action", "signing_provider": provider.name, **(metadata or {})},
    )

    return ActionProof(
        action_id=action_id,
        action_type=action_type,
        actor_id=actor_id,
        payload_hash=payload_hash,
        signature=signature,
        signer_key_id=signer.key_id,
        signing_provider=provider.name,
        zk_proof=zk_proof,
        created_at=now,
        metadata=metadata or {},
    )


def verify_proof(
    proof: ActionProof,
    payload: dict[str, Any],
    *,
    expected_actor_id: str | None = None,
    expected_action_type: str | None = None,
    signing_provider: SigningProvider | None = None,
) -> bool:
    provider = signing_provider or DEFAULT_SIGNING_PROVIDER
    computed_payload_hash = _stable_hash(payload)
    if proof.payload_hash != computed_payload_hash:
        return False

    if expected_actor_id is not None and proof.actor_id != expected_actor_id:
        return False

    if expected_action_type is not None and proof.action_type != expected_action_type:
        return False

    if proof.signing_provider != provider.name:
        return False

    if not provider.verify(proof.payload_hash, proof.signature, proof.signer_key_id):
        return False

    return verify_zk_proof(
        proof.zk_proof,
        {
            "action_id": proof.action_id,
            "action_type": proof.action_type,
            "actor_id": proof.actor_id,
            "payload_hash": proof.payload_hash,
        },
        expected_circuit=ZkCircuit.CIRC_003_ACTION_PROOF,
        expected_signer_key_id=proof.signer_key_id,
    )