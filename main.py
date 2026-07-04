# ============================================================
# CODEXIMMORTAL WARLAB — FILE METADATA HEADER
# FILE: apps/api_gateway/backend/main.py
# MODULE: API-ENTRYPOINT-REGISTRY-WIRING
# LAYER: DATA
# PURPOSE: Backend API entrypoint with validated registry bootstrap, runtime state exposure, and startup telemetry emission
# DEPENDS_ON: apps/api_gateway/backend/app_state.py, apps/api_gateway/backend/ci_registry.json, apps/api_gateway/backend/startup_telemetry.py, libs/core/ci_registry_schema.py
# EXPOSES: app
# CRYPTO_PROVENANCE: unsigned runtime entrypoint utility
# VERSION: v2
# TAG: [CODEX-TAG: CALEB-FEDOR-BYKER-KONEV-10271998-CODEXIMMORTAL]
# ============================================================

from __future__ import annotations

from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, HTTPException, Request

from app_state import AppState, bootstrap_registry_state
from core.ci_registry_schema import CiModule, find_by_code
from startup_telemetry import telemetry_json


REGISTRY_PATH = Path(__file__).with_name("ci_registry.json")


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.codex = bootstrap_registry_state(REGISTRY_PATH)
    print(telemetry_json(app.state.codex))
    yield


app = FastAPI(
    title="CodexImmortal API Gateway",
    version="v1",
    lifespan=lifespan,
)


def get_app_state(request: Request) -> AppState:
    return request.app.state.codex


@app.get("/health")
def health(request: Request) -> dict:
    state = get_app_state(request)
    return {
        "status": "ok",
        "registry_path": str(state.registry_path),
        "registry_module_count": state.registry_module_count,
    }


@app.get("/api/modules")
def list_modules(request: Request) -> list[dict]:
    state = get_app_state(request)
    return [module.model_dump() for module in state.registry.modules]


@app.get("/api/modules/{code}")
def get_module(code: str, request: Request) -> dict:
    state = get_app_state(request)
    module: CiModule | None = find_by_code(state.registry, code)
    if module is None:
        raise HTTPException(status_code=404, detail=f"module not found: {code}")
    return module.model_dump()