# ============================================================
# CODEXIMMORTAL WARLAB — FILE METADATA HEADER
# FILE: libs/core/pqc_arch.py
# MODULE: CI-001
# LAYER: PQC-SPINE
# PURPOSE: Post-quantum key lifecycle utilities, rotation planning, and HNDL exposure scan stubs for the War Lab
# DEPENDS_ON: libs/core/ci_registry_schema.py
# EXPOSES: KeyPair, RotationPolicy, HndlExposure, generate_keypair, rotate_keys, scan_hndl_exposure
# CRYPTO_PROVENANCE: unsigned development stub; interface designed for ML-KEM / ML-DSA workflows
# VERSION: v1
# TAG: [CODEX-TAG: CALEB-FEDOR-BYKER-KONEV-10271998-CODEXIMMORTAL]
# ============================================================

from __future__ import annotations

import hashlib
import secrets
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class KeyPair(BaseModel):
    model_config = ConfigDict(extra="forbid")

    key_id: str
    algorithm: Literal["ML-KEM", "ML-DSA"]
    public_key: str
    private_key_ref: str
    created_at: datetime
    expires_at: datetime
    classification: Literal["UNCLASSIFIED", "SECRET", "TS_SCI"] = "SECRET"


class RotationPolicy(BaseModel):
    model_config = ConfigDict(extra="forbid")

    session_hours: int = Field(default=24, ge=1)
    signing_days: int = Field(default=7, ge=1)
    master_days: int = Field(default=30, ge=1)
    custody_days: int = Field(default=90, ge=1)


class HndlExposure(BaseModel):
    model_config = ConfigDict(extra="forbid")

    system_name: str
    crypto_family: str
    risk_level: Literal["LOW", "MEDIUM", "HIGH", "CRITICAL"]
    migration_required: bool
    notes: str


@dataclass(slots=True)
class RotationDecision:
    key_id: str
    should_rotate: bool
    reason: str
    next_rotation_at: datetime


def _token(label: str, length: int = 32) -> str:
    material = f"{label}:{secrets.token_hex(length)}".encode()
    return hashlib.sha3_256(material).hexdigest()


def generate_keypair(
    algorithm: Literal["ML-KEM", "ML-DSA"],
    *,
    classification: Literal["UNCLASSIFIED", "SECRET", "TS_SCI"] = "SECRET",
    ttl_days: int = 30,
) -> KeyPair:
    now = datetime.now(UTC)
    key_id = f"{algorithm.lower()}-{_token('key_id', 8)[:16]}"
    return KeyPair(
        key_id=key_id,
        algorithm=algorithm,
        public_key=_token("public_key", 48),
        private_key_ref=f"vault://{key_id}/{_token('private_ref', 8)[:12]}",
        created_at=now,
        expires_at=now + timedelta(days=ttl_days),
        classification=classification,
    )


def rotate_keys(keypair: KeyPair, policy: RotationPolicy | None = None) -> RotationDecision:
    policy = policy or RotationPolicy()
    now = datetime.now(UTC)

    if keypair.algorithm == "ML-KEM":
        rotation_window = timedelta(hours=policy.session_hours)
        reason = "session encapsulation cadence"
    else:
        rotation_window = timedelta(days=policy.signing_days)
        reason = "signing key cadence"

    next_rotation_at = keypair.created_at + rotation_window
    should_rotate = now >= next_rotation_at or now >= keypair.expires_at

    if now >= keypair.expires_at:
        reason = "key expired"

    return RotationDecision(
        key_id=keypair.key_id,
        should_rotate=should_rotate,
        reason=reason,
        next_rotation_at=min(next_rotation_at, keypair.expires_at),
    )


def scan_hndl_exposure() -> list[HndlExposure]:
    return [
        HndlExposure(
            system_name="legacy-vpn-gateway",
            crypto_family="RSA-2048",
            risk_level="HIGH",
            migration_required=True,
            notes="Classical asymmetric exchange susceptible to harvest-now-decrypt-later collection.",
        ),
        HndlExposure(
            system_name="archive-signing-service",
            crypto_family="ECDSA-P256",
            risk_level="HIGH",
            migration_required=True,
            notes="Long-lived signatures should migrate to ML-DSA for post-quantum resilience.",
        ),
        HndlExposure(
            system_name="internal-session-fabric",
            crypto_family="ML-KEM",
            risk_level="LOW",
            migration_required=False,
            notes="Post-quantum exchange already in place; continue routine rotation monitoring.",
        ),
    ]