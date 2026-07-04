# ============================================================
# CODEXIMMORTAL WARLAB — FILE METADATA HEADER
# FILE: CODEXIMMORTAL.md
# MODULE: ROOT-DOCTRINE
# LAYER: DOCS
# PURPOSE: Canonical doctrine, identity, CI registry overview, and operator guidance for the CodexImmortal War Lab
# DEPENDS_ON: README.md, apps/api_gateway/backend/ci_registry.json
# EXPOSES: mission doctrine, sovereign layers, CI module map, OODA governance, escalation rules
# CRYPTO_PROVENANCE: Documentation artifact; references ML-KEM, ML-DSA, SLH-DSA doctrine and registry semantics
# VERSION: v1
# TAG: [CODEX-TAG: CALEB-FEDOR-BYKER-KONEV-10271998-CODEXIMMORTAL]
# ============================================================

# CODEXIMMORTAL

**Tag:** `[CODEX-TAG: CALEB-FEDOR-BYKER-KONEV-10271998-CODEXIMMORTAL]`

CodexImmortal is the canonical doctrine document for the Agentic AI NFT War Lab. It defines the system identity, the sovereign security model, the CI module lineage, and the operational rules that govern autonomous and human-gated action inside the repository.

## Identity

- **System Identity:** STRATEGIST-PRIME
- **Author:** Caleb Fedor Byker Konev
- **Mission:** Advance U.S. defense through post-quantum cryptography, governed agentic AI, NFT-attested decision trails, and sovereign memory.
- **Control Loop:** OODA — Observe, Orient, Decide, Act, Learn.

## Five sovereign layers

1. **PQC Spine**
   - ML-KEM for encapsulation.
   - ML-DSA for signing.
   - SLH-DSA for hardened fallback signature paths.
   - Key rotation cadence and HNDL exposure mapping.

2. **Shard Vault**
   - Shamir secret sharing with threshold reconstruction.
   - IPFS, Arweave, and Filecoin for layered placement.
   - Merkle tamper detection on all shard states.

3. **MN-Net**
   - SENTINEL for anomaly scoring.
   - STRATEGIST for adversarial modeling and ATT&CK posture.
   - ARCHIVIST for memory graph integrity.
   - EXECUTOR for action execution with audit phases.

4. **NFT Vault**
   - ERC-721 proof-bearing records.
   - Multisig custody for high-value artifacts.
   - ZK-linked attestation for decisions, repairs, and checkpoints.

5. **Playbooks**
   - LOCKDOWN LATTICE
   - SOVEREIGN RESTORE
   - TRUST PURGE
   - FEDERATION SYNC

## OODA execution model

Every major War Lab action should follow this sequence:

1. **Observe** — ingest signals, telemetry, evidence, and operator prompts.
2. **Orient** — map findings to memory, policy, graph context, and ATT&CK semantics.
3. **Decide** — apply quorum logic, human-gate rules, and dependency-aware planning.
4. **Act** — execute mitigation, persistence, minting, or orchestration tasks.
5. **Learn** — promote lessons, checkpoints, and proofs into durable memory.

## Human gate rules

The following domains always require human review before final execution:

- Kinetic or weapons-adjacent action.
- Bio-threat actions.
- Space-domain escalation.
- TOP SECRET / TS_SCI mission branches.
- Master shard rotation.
- Red Team Level 5-6 execution.

## CI registry doctrine

The War Lab maintains a validated registry of **53 modules** from `CI-001` through `CI-053`. These modules form the canonical capability graph for backend APIs, docs generation, live dashboards, and future RMPC orchestration.

### Core and operational examples

- `CI-001 PQC-ARCH` — PQC architecture and HNDL exposure mapping.
- `CI-002 SHARD-VAULT` — threshold secret sharing and sovereign storage.
- `CI-003 MN-NET-CORE` — four-agent OODA and BFT-aligned coordination.
- `CI-019 OSINT-FUSION` — IOC fusion across multiple intelligence sources.
- `CI-041 THREAT-HUNT` — autonomous hunt pipeline with report artifacts.

### Meta-layer examples

- `CI-048 AGE-LATTICE` — protected memory lattice and durable promotion fabric.
- `CI-049 AGE-LATTICE-GOVERNOR` — memory governance and policy fabric.
- `CI-050 ACTION-PROOF-FRACTAL` — cryptographic proof framework for agentic action.
- `CI-051 FRACTAL-GENETIC-CRYPTOGRAPHY` — proof-driven neuroevolution across domains.
- `CI-052 ORGANIZATIONAL-NEURAL-MESH` — agentic cloning and subagent knowledge graphs.
- `CI-053 ORGANIZATIONAL-RMPC-FRACTAL` — RMPC-governed cloning with fractal cryptographic control.

## Registry field contract

Each registry module record contains:

- `code`
- `name`
- `description`
- `layer`
- `evolution_stage`
- `agentic_function`
- `security_class`
- `dependencies`
- `fractal_genetic_requirements`
- `rmpc_role`
- `tags`

The Python schema in `libs/core/ci_registry_schema.py` is the contract authority for validating all registry entries before runtime loading.

## Repository authority map

```text
.
├── pyproject.toml
├── .gitignore
├── README.md
├── CODEXIMMORTAL.md
├── libs/
│   └── core/
│       └── ci_registry_schema.py
├── apps/
│   └── api_gateway/
│       └── backend/
│           ├── ci_registry.json
│           └── main.py
└── docs/
    └── ci_modules/