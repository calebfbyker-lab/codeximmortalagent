# ============================================================
# CODEXIMMORTAL WARLAB — FILE METADATA HEADER
# FILE: scripts/update_build_state.py
# MODULE: BUILD-STATE-AUTO-UPDATER
# LAYER: DOCS
# PURPOSE: Regenerate build_state.json and build_state.md from a curated completion list and the master manifest blueprint
# DEPENDS_ON: docs/file_manifest.md
# EXPOSES: main(), load_completion_map(), render_build_state_json(), render_build_state_md()
# CRYPTO_PROVENANCE: unsigned utility script
# VERSION: v1
# TAG: [CODEX-TAG: CALEB-FEDOR-BYKER-KONEV-10271998-CODEXIMMORTAL]
# ============================================================

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List


TAG = "[CODEX-TAG: CALEB-FEDOR-BYKER-KONEV-10271998-CODEXIMMORTAL]"


@dataclass
class FileStatus:
    path: str
    status: str
    dependency_ready: bool
    notes: str


@dataclass
class GroupStatus:
    group: str
    scope: str
    status: str
    notes: str


def load_completion_map() -> Dict[str, FileStatus]:
    return {
        "docs/file_manifest.md": FileStatus(
            path="docs/file_manifest.md",
            status="complete",
            dependency_ready=True,
            notes="Canonical blueprint and progress map established.",
        ),
        "libs/core/ci_registry_schema.py": FileStatus(
            path="libs/core/ci_registry_schema.py",
            status="complete",
            dependency_ready=True,
            notes="Schema and helper surface available.",
        ),
        "libs/core/pqc_arch.py": FileStatus(
            path="libs/core/pqc_arch.py",
            status="complete",
            dependency_ready=True,
            notes="PQC support scaffold available.",
        ),
        "libs/core/zk_proof.py": FileStatus(
            path="libs/core/zk_proof.py",
            status="complete",
            dependency_ready=True,
            notes="ZK abstraction stub available.",
        ),
        "libs/core/action_proof.py": FileStatus(
            path="libs/core/action_proof.py",
            status="complete",
            dependency_ready=True,
            notes="Proof model and provider wiring implemented.",
        ),
        "apps/api_gateway/backend/ci_registry.json": FileStatus(
            path="apps/api_gateway/backend/ci_registry.json",
            status="complete",
            dependency_ready=True,
            notes="Validated module registry present.",
        ),
        "apps/api_gateway/backend/main.py": FileStatus(
            path="apps/api_gateway/backend/main.py",
            status="complete",
            dependency_ready=True,
            notes="FastAPI entrypoint with health and module endpoints present.",
        ),
        "apps/api_gateway/backend/startup_telemetry.py": FileStatus(
            path="apps/api_gateway/backend/startup_telemetry.py",
            status="complete",
            dependency_ready=True,
            notes="Schema-versioned startup telemetry implemented.",
        ),
        "apps/frontend/src/App.tsx": FileStatus(
            path="apps/frontend/src/App.tsx",
            status="complete",
            dependency_ready=True,
            notes="Dashboard shell with registry fetch and filtering exists.",
        ),
        "apps/frontend/src/styles.css": FileStatus(
            path="apps/frontend/src/styles.css",
            status="complete",
            dependency_ready=True,
            notes="Initial frontend visual layer implemented.",
        ),
        "libs/age_lattice/memory_actions.py": FileStatus(
            path="libs/age_lattice/memory_actions.py",
            status="pending",
            dependency_ready=True,
            notes="Recommended next file.",
        ),
        "libs/age_lattice/metrics.py": FileStatus(
            path="libs/age_lattice/metrics.py",
            status="pending",
            dependency_ready=False,
            notes="Depends on memory actions model choices.",
        ),
        "libs/age_lattice/policy_engine.py": FileStatus(
            path="libs/age_lattice/policy_engine.py",
            status="pending",
            dependency_ready=False,
            notes="Depends on age lattice models.",
        ),
        "libs/orchestrator/rmpc_controller.py": FileStatus(
            path="libs/orchestrator/rmpc_controller.py",
            status="pending",
            dependency_ready=False,
            notes="Blocked by agent genome and optimizer layers.",
        ),
        "infra/docker/docker-compose.yml": FileStatus(
            path="infra/docker/docker-compose.yml",
            status="pending",
            dependency_ready=False,
            notes="Blocked by backend/frontend/infra stabilization.",
        ),
    }


def group_statuses() -> List[GroupStatus]:
    return [
        GroupStatus(
            group="A",
            scope="Root config/docs",
            status="partial",
            notes="Master manifest exists, but root workspace and operator docs remain unfinished.",
        ),
        GroupStatus(
            group="B",
            scope="libs/core",
            status="complete",
            notes="Core schema, PQC, ZK, action proof, and tests are implemented.",
        ),
        GroupStatus(
            group="C",
            scope="backend registry JSON",
            status="complete",
            notes="Registry JSON exists and is validated by backend startup tooling.",
        ),
        GroupStatus(
            group="D",
            scope="libs/age_lattice",
            status="pending",
            notes="Memory governance layer not yet implemented.",
        ),
        GroupStatus(
            group="E",
            scope="libs/knowledge_graph",
            status="pending",
            notes="Graph models, Merkle index, and storage wrapper not yet implemented.",
        ),
        GroupStatus(
            group="F",
            scope="libs/orchestrator",
            status="pending",
            notes="Agent genome, optimizer, RMPC, and organizational agent are pending.",
        ),
        GroupStatus(
            group="G",
            scope="backend wiring",
            status="partial",
            notes="Simplified main entrypoint and telemetry routes exist, but split adapters/routes are pending.",
        ),
        GroupStatus(
            group="H",
            scope="frontend app",
            status="partial",
            notes="Vite React shell and dashboard UI exist, but API abstraction and component decomposition are pending.",
        ),
        GroupStatus(
            group="I",
            scope="infra",
            status="pending",
            notes="Docker, SQL schema, migrations, and NGINX are not yet implemented.",
        ),
        GroupStatus(
            group="J",
            scope="scripts/docs/integration",
            status="partial",
            notes="Manifest exists, but launcher scripts and full integration tests are pending.",
        ),
    ]


def render_build_state_json(files: Dict[str, FileStatus], groups: List[GroupStatus]) -> str:
    completed_groups = sum(1 for g in groups if g.status == "complete")
    partial_groups = sum(1 for g in groups if g.status == "partial")
    pending_groups = sum(1 for g in groups if g.status == "pending")

    recommended_next_group = "D"
    recommended_next_files = [
        "libs/age_lattice/memory_actions.py",
        "libs/age_lattice/metrics.py",
        "libs/age_lattice/policy_engine.py",
        "libs/age_lattice/tests/test_policy_engine.py",
    ]

    payload = {
        "tag": TAG,
        "version": "v1",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "summary": {
            "total_manifest_groups": len(groups),
            "completed_groups": completed_groups,
            "partial_groups": partial_groups,
            "pending_groups": pending_groups,
            "recommended_next_group": recommended_next_group,
            "recommended_next_files": recommended_next_files,
        },
        "groups": [
            {
                "group": g.group,
                "scope": g.scope,
                "status": g.status,
                "notes": g.notes,
            }
            for g in groups
        ],
        "files": [
            {
                "path": fs.path,
                "status": fs.status,
                "dependency_ready": fs.dependency_ready,
                "notes": fs.notes,
            }
            for fs in files.values()
        ],
    }

    return json.dumps(payload, indent=2)


def render_build_state_md(files: Dict[str, FileStatus], groups: List[GroupStatus]) -> str:
    lines: List[str] = []
    lines.append("# ============================================================")
    lines.append("# CODEXIMMORTAL WARLAB — FILE METADATA HEADER")
    lines.append("# FILE: docs/build_state.md")
    lines.append("# MODULE: BUILD-STATE-LEDGER")
    lines.append("# LAYER: DOCS")
    lines.append("# PURPOSE: Human-readable build-state ledger synchronized to the master manifest")
    lines.append("# DEPENDS_ON: docs/file_manifest.md, docs/build_state.json")
    lines.append("# EXPOSES: current repo status, next recommended file group, dependency readiness notes")
    lines.append("# CRYPTO_PROVENANCE: unsigned documentation artifact")
    lines.append("# VERSION: v1")
    lines.append(f"# TAG: {TAG}")
    lines.append("# ============================================================")
    lines.append("")
    lines.append("# CodexImmortal Build State Ledger")
    lines.append("")
    lines.append(
        "This ledger translates the master manifest into a current-state planning view so operators and agents can determine the next valid build step quickly."
    )
    lines.append("")

    completed_groups = sum(1 for g in groups if g.status == "complete")
    partial_groups = sum(1 for g in groups if g.status == "partial")
    pending_groups = sum(1 for g in groups if g.status == "pending")

    lines.append("## Summary")
    lines.append("")
    lines.append(f"- Total manifest groups: {len(groups)}")
    lines.append(f"- Completed groups: {completed_groups}")
    lines.append(f"- Partial groups: {partial_groups}")
    lines.append(f"- Pending groups: {pending_groups}")
    lines.append("- Recommended next group: **D — `libs/age_lattice`**")
    lines.append("- Recommended next files:")
    lines.append("  - `libs/age_lattice/memory_actions.py`")
    lines.append("  - `libs/age_lattice/metrics.py`")
    lines.append("  - `libs/age_lattice/policy_engine.py`")
    lines.append("  - `libs/age_lattice/tests/test_policy_engine.py`")
    lines.append("")

    lines.append("## Group status")
    lines.append("")
    lines.append("| Group | Scope | Status | Notes |")
    lines.append("|---|---|---|---|")
    for g in groups:
        lines.append(f"| {g.group} | {g.scope} | {g.status} | {g.notes} |")
    lines.append("")

    lines.append("## File readiness snapshot")
    lines.append("")
    lines.append("| File | Status | Dependency ready | Notes |")
    lines.append("|---|---|---:|---|")
    for fs in files.values():
        ready = "yes" if fs.dependency_ready else "no"
        lines.append(f"| `{fs.path}` | {fs.status} | {ready} | {fs.notes} |")
    lines.append("")

    lines.append("## Build interpretation")
    lines.append("")
    lines.append(
        "The repo already supports a thin end-to-end path from registry data to FastAPI delivery to a React dashboard view. "
        "The next highest-leverage step is to build the memory-governance layer so the repo can evolve beyond registry visibility "
        "into policy-bearing agent behavior."
    )
    lines.append("")

    return "
".join(lines)


def main() -> None:
    files = load_completion_map()
    groups = group_statuses()

    json_payload = render_build_state_json(files, groups)
    md_payload = render_build_state_md(files, groups)

    docs_dir = Path("docs")
    docs_dir.mkdir(parents=True, exist_ok=True)

    (docs_dir / "build_state.json").write_text(json_payload)
    (docs_dir / "build_state.md").write_text(md_payload)


if __name__ == "__main__":
    main()