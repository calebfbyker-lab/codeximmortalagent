# ============================================================
# CODEXIMMORTAL WARLAB — FILE METADATA HEADER
# FILE: libs/core/zk_proof.py
# MODULE: CI-005
# LAYER: NFT-VAULT
# PURPOSE: Zero-knowledge circuit registry and provider-backed proof create/verify stubs for War Lab attestation flows
# DEPENDS_ON: libs/core/pqc_arch.py
# EXPOSES: ZkCircuit, ZkProof, ZkBackend, MockZkBackend, create_zk_proof, verify_zk_proof, list_supported_circuits
# CRYPTO_PROVENANCE: unsigned development stub; interface designed for Groth16 / PLONK / STARK workflows
# VERSION: v2
# TAG: [CODEX-TAG: CALEB-FEDOR-BYKER-KONEV-10271998-CODEXIMMORTAL]
# ============================================================

from __future__ import annotations

import hashlib
import json
from datetime import UTC, datetime
from enum import Enum
from typing import Any, Literal, Protocol

from pydantic import BaseModel, ConfigDict, Field

from core.pqc_arch import KeyPair


class ZkCircuit(str, Enum):
    CIRC_001_EVENT_ATTESTATION = "CIRC-001-EVENT-ATTESTATION"
    CIRC_002_MEMORY_ROOT = "CIRC-002-MEMORY-ROOT"
    CIRC_003_ACTION_PROOF = "CIRC-003-ACTION-PROOF"
    CIRC_004_LINEAGE_PROMOTION = "CIRC-004-LINEAGE-PROMOTION"
    CIRC_005_SHARD_INTEGRITY = "CIRC-005-SHARD-INTEGRITY"
    CIRC_006_THREAT_VERDICT = "CIRC-006-THREAT-VERDICT"
    CIRC_007_MODEL_CHECKPOINT = "CIRC-007-MODEL-CHECKPOINT"


class ZkProof(BaseModel):
    model_config = ConfigDict(extra="forbid")

    proof_id: str
    circuit: ZkCircuit
    proving_system: Literal["Groth16", "PLONK", "STARK"]
    public_inputs_hash: str
    witness_hash: str
    proof_blob: str
    verification_key_ref: str
    signer_key_id: str
    created_at: datetime
    backend_name: str = "mock"
    metadata: dict[str, Any] = Field(default_factory=dict)


class ZkBackend(Protocol):
    name: str

    def create_proof(
        self,
        circuit: ZkCircuit,
        public_inputs: dict[str, Any],
        witness: dict[str, Any],
        signer: KeyPair,
        *,
        proving_system: Literal["Groth16", "PLONK", "STARK"],
        metadata: dict[str, Any] | None = None,
    ) -> ZkProof: ...

    def verify_proof(
        self,
        proof: ZkProof,
        public_inputs: dict[str, Any],
        *,
        expected_circuit: ZkCircuit | None = None,
        expected_signer_key_id: str | None = None,
    ) -> bool: ...


class MockZkBackend:
    name = "mock"

    @staticmethod
    def _stable_hash(payload: Any) -> str:
        encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str).encode()
        return hashlib.sha3_256(encoded).hexdigest()

    def create_proof(
        self,
        circuit: ZkCircuit,
        public_inputs: dict[str, Any],
        witness: dict[str, Any],
        signer: KeyPair,
        *,
        proving_system: Literal["Groth16", "PLONK", "STARK"],
        metadata: dict[str, Any] | None = None,
    ) -> ZkProof:
        now = datetime.now(UTC)
        public_inputs_hash = self._stable_hash(public_inputs)
        witness_hash = self._stable_hash(witness)
        proof_material = {
            "circuit": circuit.value,
            "proving_system": proving_system,
            "public_inputs_hash": public_inputs_hash,
            "witness_hash": witness_hash,
            "signer_key_id": signer.key_id,
            "created_at": now.isoformat(),
            "backend_name": self.name,
        }
        proof_id = f"zk-{self._stable_hash(proof_material)[:16]}"

        return ZkProof(
            proof_id=proof_id,
            circuit=circuit,
            proving_system=proving_system,
            public_inputs_hash=public_inputs_hash,
            witness_hash=witness_hash,
            proof_blob=self._stable_hash({"proof_material": proof_material, "metadata": metadata or {}}),
            verification_key_ref=f"vk://{circuit.value.lower()}/{proving_system.lower()}",
            signer_key_id=signer.key_id,
            created_at=now,
            backend_name=self.name,
            metadata=metadata or {},
        )

    def verify_proof(
        self,
        proof: ZkProof,
        public_inputs: dict[str, Any],
        *,
        expected_circuit: ZkCircuit | None = None,
        expected_signer_key_id: str | None = None,
    ) -> bool:
        if expected_circuit is not None and proof.circuit != expected_circuit:
            return False
        if expected_signer_key_id is not None and proof.signer_key_id != expected_signer_key_id:
            return False
        if proof.public_inputs_hash != self._stable_hash(public_inputs):
            return False
        if not proof.proof_id.startswith("zk-"):
            return False
        if not proof.verification_key_ref.startswith("vk://"):
            return False
        if proof.backend_name != self.name:
            return False
        return True


DEFAULT_BACKEND: ZkBackend = MockZkBackend()


def list_supported_circuits() -> list[str]:
    return [circuit.value for circuit in ZkCircuit]


def create_zk_proof(
    circuit: ZkCircuit,
    public_inputs: dict[str, Any],
    witness: dict[str, Any],
    signer: KeyPair,
    *,
    proving_system: Literal["Groth16", "PLONK", "STARK"] = "Groth16",
    metadata: dict[str, Any] | None = None,
    backend: ZkBackend | None = None,
) -> ZkProof:
    engine = backend or DEFAULT_BACKEND
    return engine.create_proof(
        circuit,
        public_inputs,
        witness,
        signer,
        proving_system=proving_system,
        metadata=metadata,
    )


def verify_zk_proof(
    proof: ZkProof,
    public_inputs: dict[str, Any],
    *,
    expected_circuit: ZkCircuit | None = None,
    expected_signer_key_id: str | None = None,
    backend: ZkBackend | None = None,
) -> bool:
    engine = backend or DEFAULT_BACKEND
    return engine.verify_proof(
        proof,
        public_inputs,
        expected_circuit=expected_circuit,
        expected_signer_key_id=expected_signer_key_id,
    )