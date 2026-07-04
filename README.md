# codeximmortalagent
# ============================================================
# CODEXIMMORTAL WARLAB — FILE METADATA HEADER
# FILE: README.md
# MODULE: ROOT-WORKSPACE
# LAYER: DOCS
# PURPOSE: Root project overview for the CodexImmortal Agentic AI NFT War Lab monorepo
# DEPENDS_ON: pyproject.toml, apps/api_gateway/backend/ci_registry.json
# EXPOSES: architecture overview, repo layout, quickstart, CI module map
# CRYPTO_PROVENANCE: ML-DSA doctrine referenced; documentation artifact only
# VERSION: v1
# TAG: [CODEX-TAG: CALEB-FEDOR-BYKER-KONEV-10271998-CODEXIMMORTAL]
# ============================================================

# CodexImmortal Agentic AI NFT War Lab

Defense-native R&D environment for governed, cryptographically-attested, post-quantum agentic AI. The War Lab is designed to transform autonomous systems from opaque tools into auditable, sovereign, multi-agent infrastructure with post-quantum trust, zero-knowledge verification, and operator-controlled escalation paths.

## Mission

The War Lab advances U.S. defense-oriented AI through five sovereign layers:

1. **PQC Spine** — ML-KEM, ML-DSA, SLH-DSA, rekey policy, HNDL migration.
2. **Shard Vault** — Shamir secret sharing, Merkle tamper detection, IPFS/Arweave/Filecoin placement.
3. **MN-Net** — SENTINEL, STRATEGIST, ARCHIVIST, EXECUTOR under OODA and BFT-style consensus.
4. **NFT Vault** — ERC-721 attestation, multisig custody, proof-linked decision artifacts.
5. **Playbooks** — LOCKDOWN LATTICE, SOVEREIGN RESTORE, TRUST PURGE, FEDERATION SYNC.

## Current module scope

This repository tracks a machine-readable registry of **53 modules** from `CI-001` through `CI-053`, spanning PQC lifecycle management, sovereign storage, OSINT fusion, autonomous threat hunting, memory governance, RMPC-controlled cloning, and fractal genetic cryptography.

Representative modules include:

- `CI-001 PQC-ARCH` — ML-KEM / ML-DSA key lifecycle and HNDL exposure mapping.
- `CI-003 MN-NET-CORE` — four-agent consensus and OODA execution fabric.
- `CI-019 OSINT-FUSION` — multi-source IOC collection and fusion scoring.
- `CI-041 THREAT-HUNT` — autonomous threat hunting and HuntReport NFT issuance.
- `CI-053 ORGANIZATIONAL-RMPC-FRACTAL` — RMPC-governed cloning with fractal cryptographic control.

## Repository layout

```text
.
├── pyproject.toml
├── README.md
├── libs/
│   ├── core/
│   ├── age_lattice/
│   ├── orchestrator/
│   └── knowledge_graph/
├── apps/
│   └── api_gateway/
│       └── backend/
│           ├── main.py
│           ├── ci_registry.json
│           └── routers/
├── docs/
│   └── ci_modules/
└── tests/