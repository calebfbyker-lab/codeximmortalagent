# ============================================================
# CODEXIMMORTAL WARLAB — FILE METADATA HEADER
# FILE: AGENTS.md
# MODULE: AGENT-GOVERNANCE
# LAYER: ORCHESTRATOR
# PURPOSE: Define what human and software agents may read, write, execute, or modify across the monorepo
# DEPENDS_ON: CODEXIMMORTAL.md, README.md, libs/core/ci_registry_schema.py
# EXPOSES: directory-level governance rules, execution constraints, copy-paste build protocol, human-gate policy
# CRYPTO_PROVENANCE: unsigned documentation artifact; operational references align to ML-DSA / Merkle / ZK governance doctrine
# VERSION: v1
# TAG: [CODEX-TAG: CALEB-FEDOR-BYKER-KONEV-10271998-CODEXIMMORTAL]
# ============================================================

# AGENTS.md

This file defines repository governance for human operators, coding agents, orchestration agents, and documentation agents working inside the CodexImmortal Warlab Python monorepo.

## Operating doctrine

All agent behavior inside this repository follows five non-negotiable rules:

1. **Schema before runtime** — data contracts must exist before services that consume them.
2. **Copy-pasteable assembly** — every file must be emitted in a complete form so it can be directly pasted into the repository without reconstruction.
3. **Header-first identity** — every source, config, SQL, shell, and docs file must begin with the standardized metadata header.
4. **Dependency-ordered construction** — files are created only after their declared dependencies exist.
5. **Human gate for high-consequence changes** — changes touching secrets, custody, destruction, bio, space, weapons, or master rotation require explicit operator review.

## Agent roles

| Agent Type | Primary Function | Allowed Scope | Restricted Actions |
|---|---|---|---|
| Documentation Agent | Generate markdown, manifests, architecture docs | `README.md`, `CODEXIMMORTAL.md`, `docs/` | Cannot alter runtime policy or secret material |
| Core Code Agent | Build schemas, proof utilities, PQC helpers | `libs/core/` | Cannot bypass tests or relax validation silently |
| Memory Agent | Build Age Lattice memory policy modules | `libs/age_lattice/`, `apps/api_gateway/backend/age_lattice_adapter.py` | Cannot persist undocumented personal or classified data paths |
| Orchestrator Agent | Build RMPC, genome, genetic optimization logic | `libs/orchestrator/`, `apps/api_gateway/backend/orchestrator_rmpc.py` | Cannot enable autonomous high-risk execution without gate logic |
| Graph Agent | Build knowledge graph models and storage adapters | `libs/knowledge_graph/`, `apps/api_gateway/backend/knowledge_graph_api.py` | Cannot remove proof linkage from graph writes |
| API Agent | Build backend routes, adapters, FastAPI app, WS handlers | `apps/api_gateway/backend/` | Cannot expose unsafe admin mutation endpoints by default |
| Dashboard Agent | Build frontend dashboard components and API clients | `apps/dashboard/` | Cannot hardcode secrets or bypass backend policy checks |
| Infra Agent | Build Docker, NGINX, DB schema, compose files | `infra/`, `scripts/` | Cannot embed plaintext secrets or production credentials |
| Test Agent | Build unit/integration tests | `tests/`, `libs/*/tests`, `apps/*/tests` | Cannot rewrite source behavior to fit failing tests |

## Directory governance map

| Directory / File | Purpose | Allowed Actions | Constraints |
|---|---|---|---|
| `pyproject.toml` | Root workspace configuration | Read, update deps, tune tooling | Keep Python version and workspace package list consistent |
| `.gitignore` | Secret and artifact exclusion | Read, append ignore rules | Never remove secret-protection entries without human review |
| `README.md` | Public project overview | Read, update docs | Keep consistent with actual implemented structure |
| `CODEXIMMORTAL.md` | Canonical doctrine | Read, extend doctrine | Doctrine changes affecting control policy require review |
| `AGENTS.md` | Agent governance file | Read, update constraints | Must remain stricter than implementation, not looser |
| `libs/core/` | Shared schema and proof primitives | Read, write, test | Breaking schema changes require dependent review |
| `libs/age_lattice/` | Memory policy logic | Read, write, test | Preserve pure-function policy logic where possible |
| `libs/orchestrator/` | RMPC and genetic orchestration | Read, write, test | No autonomous execution paths without explicit guardrails |
| `libs/knowledge_graph/` | Graph models and storage | Read, write, test | Maintain provenance and Merkle integrity hooks |
| `apps/api_gateway/backend/ci_registry.json` | Canonical CI capability data | Read, validate, regenerate | Must validate against `CiRegistry` before use |
| `apps/api_gateway/backend/routes/` | API routing layer | Read, write, test | Routes must stay thin; business logic lives in libs/adapters |
| `apps/dashboard/` | Frontend views and clients | Read, write, test | UI may visualize state but not redefine policy |
| `infra/` | Deployment and persistence plumbing | Read, write, test | Avoid environment-specific secrets and hardcoded tokens |
| `docs/` | Human-readable docs and manifests | Read, write | Keep synced with machine-readable contracts |
| `scripts/` | Developer automation | Read, write | Scripts must be local-safe and idempotent where feasible |
| `tests/` | Verification | Read, write | Tests should validate expected behavior, not encode hidden assumptions |

## Required file structure standard

Every newly created file must follow this pattern:

1. Metadata header.
2. Imports or opening declarations.
3. Type definitions or schema models.
4. Primary implementation.
5. Minimal runnable example or tests where appropriate.

For documentation files, the structure is:

1. Metadata header.
2. Title.
3. Purpose or doctrine summary.
4. Structured sections.
5. Copy-pasteable examples when relevant.

## Build protocol

Agents must build the repository in manifest order. The current top-level sequence is:

1. `pyproject.toml`
2. `.gitignore`
3. `README.md`
4. `CODEXIMMORTAL.md`
5. `AGENTS.md`
6. `Makefile`
7. `libs/core/ci_registry_schema.py`
8. `libs/core/pqc_arch.py`
9. `libs/core/zk_proof.py`
10. `libs/core/action_proof.py`
11. tests for `libs/core`
12. `apps/api_gateway/backend/ci_registry.json`
13. age lattice, graph, orchestrator, backend, dashboard, infra, docs, scripts, integration tests

No agent should skip forward if doing so would create a dependency inversion.

## Editing constraints

- Do not emit partial snippets when a full file is requested.
- Do not invent dependencies that are not declared in the manifest or doctrine.
- Do not introduce secret values, API keys, private endpoints, or local file paths containing sensitive material.
- Do not silently downgrade validation, classification handling, or human-gate logic.
- Do not collapse `libs/` and `apps/` boundaries by moving core logic into route files.

## Human gate conditions

The following changes must be escalated for human review before merge:

- Any addition of secret material handling beyond placeholders.
- Any change to shard recovery, custody rotation, multisig, or key lifecycle semantics.
- Any route or function enabling destructive actions.
- Any autonomous action path for kinetic, navigation, fire-control, space, or bio domains.
- Any weakening of schema validation or audit/provenance hooks.

## Validation expectations

Agents should validate work incrementally:

- After schema files: run unit tests for the schema.
- After proof files: run proof-related tests.
- After adapters/routes: run backend tests.
- After frontend files: run type/build checks.
- After infra files: validate container and proxy syntax.

## Coding curriculum

### Concept: monorepo boundary discipline

Monorepo boundary discipline means each directory has a clear responsibility and stable dependency direction. In the War Lab, this matters because orchestration, cryptography, memory, graph state, and API surfaces must evolve independently without collapsing into one unsafe control blob.

Minimal runnable example:

```python
# cryptographic provenance: boundary discipline example
from core.ci_registry_schema import load_registry

modules = [{
    "code": "CI-001",
    "name": "PQC-ARCH",
    "description": "Boundary discipline demo.",
    "layer": "PQC-SPINE",
    "evolution_stage": "core",
    "agentic_function": "crypto",
    "security_class": "TS_SCI",
    "dependencies": [],
    "fractal_genetic_requirements": {
        "signing": "ML-DSA",
        "root_level": "agent",
        "merkle_required": True,
        "zk_required": True
    },
    "rmpc_role": "state",
    "tags": ["boundary", "schema"]
}]

registry = load_registry(modules)
assert registry.modules.layer == "PQC-SPINE"

## Placement

Save this as `AGENTS.md` at the repository root beside `README.md` and `CODEXIMMORTAL.md`. It acts as the governance contract for future file generation and agent behavior across the monorepo. 

[CODEX-TAG: CALEB-FEDOR-BYKER-KONEV-10271998-CODEXIMMORTAL]

--------------------------------------------------
CODEX EVOLUTION PROPOSAL
Proposed By: STRATEGIST-PRIME
CAPABILITY: Agent Policy Enforcement Layer
LAYER: ORCHESTRATOR
TRIGGER: Governance rules now exist in documentation, but they are not yet machine-enforced during file generation or code review.
DESCRIPTION: Add a lightweight policy checker that validates required file headers, declared dependency order, and forbidden secret patterns before commits or generated outputs are accepted. This turns `AGENTS.md` from static guidance into an enforceable build discipline layer.
IMPLEMENTATION:
  Phase 1 [AUTOMATED]: Create a script that scans files for required header fields and forbidden patterns.
  Phase 2 [HUMAN GATE]: Review exception cases for generated files, vendor assets, and third-party examples.
  Phase 3 [AUDIT STAMP]: Anchor policy-check results and manifest hashes into the provenance ledger.
PAYOFF DELTA: Shield Score +2 | Vault Shards +160 | Neural Peers +20
--------------------------------------------------