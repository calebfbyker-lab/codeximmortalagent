import { useEffect, useMemo, useState } from "react";

type FractalRequirements = {
  signing: string;
  root_level: string;
  merkle_required: boolean;
  zk_required: boolean;
};

type ModuleRecord = {
  code: string;
  name: string;
  description: string;
  layer: string;
  evolution_stage: string;
  agentic_function: string;
  security_class: string;
  dependencies: string[];
  fractal_genetic_requirements: FractalRequirements;
  rmpc_role: string;
  tags: string[];
};

type HealthPayload = {
  schema_version: string;
  status: string;
  registry_path: string;
  registry_module_count: number;
  validated_at: string;
};

const API_BASE = import.meta.env.VITE_API_BASE_URL ?? "http://127.0.0.1:8000";

function App() {
  const [modules, setModules] = useState<ModuleRecord[]>([]);
  const [health, setHealth] = useState<HealthPayload | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedStage, setSelectedStage] = useState<string>("all");
  const [selectedModuleCode, setSelectedModuleCode] = useState<string | null>(null);

  useEffect(() => {
    async function load() {
      try {
        setLoading(true);
        setError(null);

        const [healthResponse, modulesResponse] = await Promise.all([
          fetch(`${API_BASE}/health`),
          fetch(`${API_BASE}/api/modules`),
        ]);

        if (!healthResponse.ok) {
          throw new Error(`Health request failed: ${healthResponse.status}`);
        }
        if (!modulesResponse.ok) {
          throw new Error(`Modules request failed: ${modulesResponse.status}`);
        }

        const healthPayload: HealthPayload = await healthResponse.json();
        const modulesPayload: ModuleRecord[] = await modulesResponse.json();

        setHealth(healthPayload);
        setModules(modulesPayload);
        setSelectedModuleCode((current) => current ?? modulesPayload[0]?.code ?? null);
      } catch (err) {
        setError(err instanceof Error ? err.message : "Unknown frontend load failure");
      } finally {
        setLoading(false);
      }
    }

    load();
  }, []);

  const stages = useMemo(() => {
    const values = new Set(modules.map((module) => module.evolution_stage));
    return ["all", ...Array.from(values)];
  }, [modules]);

  const filteredModules = useMemo(() => {
    if (selectedStage === "all") {
      return modules;
    }
    return modules.filter((module) => module.evolution_stage === selectedStage);
  }, [modules, selectedStage]);

  const selectedModule = useMemo(() => {
    return filteredModules.find((module) => module.code === selectedModuleCode) ?? filteredModules[0] ?? null;
  }, [filteredModules, selectedModuleCode]);

  return (
    <div className="app-shell">
      <header className="hero">
        <div>
          <p className="eyebrow">CodexImmortal War Lab</p>
          <h1>Defense registry command surface</h1>
          <p className="hero-copy">
            Frontend visibility layer for CI modules, telemetry-backed health, and fast inspection of sovereign defense capabilities.
          </p>
        </div>
        <div className="hero-card">
          <p className="card-label">Backend status</p>
          <strong>{health?.status ?? "loading"}</strong>
          <span>Schema {health?.schema_version ?? "--"}</span>
          <span>{health ? `${health.registry_module_count} modules validated` : "Awaiting registry"}</span>
        </div>
      </header>

      {loading ? <section className="panel">Loading CodexImmortal frontend…</section> : null}
      {error ? <section className="panel error-panel">{error}</section> : null}

      {!loading && !error ? (
        <main className="dashboard-grid">
          <section className="panel">
            <div className="panel-header">
              <h2>Registry health</h2>
              <span className="badge">{health?.schema_version ?? "unknown schema"}</span>
            </div>
            <dl className="metric-grid">
              <div>
                <dt>Status</dt>
                <dd>{health?.status ?? "unknown"}</dd>
              </div>
              <div>
                <dt>Validated</dt>
                <dd>{health?.validated_at ? new Date(health.validated_at).toLocaleString() : "n/a"}</dd>
              </div>
              <div>
                <dt>Registry path</dt>
                <dd>{health?.registry_path ?? "n/a"}</dd>
              </div>
              <div>
                <dt>Module count</dt>
                <dd>{health?.registry_module_count ?? 0}</dd>
              </div>
            </dl>
          </section>

          <section className="panel">
            <div className="panel-header">
              <h2>Stage filter</h2>
              <span className="badge">{filteredModules.length} visible</span>
            </div>
            <div className="filter-row">
              {stages.map((stage) => (
                <button
                  key={stage}
                  className={stage === selectedStage ? "filter-pill active" : "filter-pill"}
                  onClick={() => setSelectedStage(stage)}
                >
                  {stage}
                </button>
              ))}
            </div>
          </section>

          <section className="panel list-panel">
            <div className="panel-header">
              <h2>CI modules</h2>
              <span className="badge">{filteredModules.length}</span>
            </div>
            <div className="module-list">
              {filteredModules.map((module) => (
                <button
                  key={module.code}
                  className={module.code === selectedModule?.code ? "module-row active" : "module-row"}
                  onClick={() => setSelectedModuleCode(module.code)}
                >
                  <span>
                    <strong>{module.code}</strong>
                    <small>{module.name}</small>
                  </span>
                  <span>{module.security_class}</span>
                </button>
              ))}
            </div>
          </section>

          <section className="panel detail-panel">
            <div className="panel-header">
              <h2>Module detail</h2>
              <span className="badge">{selectedModule?.layer ?? "none selected"}</span>
            </div>
            {selectedModule ? (
              <div className="detail-stack">
                <div>
                  <p className="eyebrow">{selectedModule.code}</p>
                  <h3>{selectedModule.name}</h3>
                  <p>{selectedModule.description}</p>
                </div>

                <div className="detail-grid">
                  <div>
                    <dt>Stage</dt>
                    <dd>{selectedModule.evolution_stage}</dd>
                  </div>
                  <div>
                    <dt>Function</dt>
                    <dd>{selectedModule.agentic_function}</dd>
                  </div>
                  <div>
                    <dt>Security</dt>
                    <dd>{selectedModule.security_class}</dd>
                  </div>
                  <div>
                    <dt>RMPC role</dt>
                    <dd>{selectedModule.rmpc_role}</dd>
                  </div>
                </div>

                <div>
                  <h4>Dependencies</h4>
                  <div className="tag-wrap">
                    {selectedModule.dependencies.length ? (
                      selectedModule.dependencies.map((dependency) => <span key={dependency} className="tag">{dependency}</span>)
                    ) : (
                      <span className="tag">No dependencies</span>
                    )}
                  </div>
                </div>

                <div>
                  <h4>Fractal requirements</h4>
                  <div className="detail-grid">
                    <div>
                      <dt>Signing</dt>
                      <dd>{selectedModule.fractal_genetic_requirements.signing}</dd>
                    </div>
                    <div>
                      <dt>Root level</dt>
                      <dd>{selectedModule.fractal_genetic_requirements.root_level}</dd>
                    </div>
                    <div>
                      <dt>Merkle required</dt>
                      <dd>{selectedModule.fractal_genetic_requirements.merkle_required ? "Yes" : "No"}</dd>
                    </div>
                    <div>
                      <dt>ZK required</dt>
                      <dd>{selectedModule.fractal_genetic_requirements.zk_required ? "Yes" : "No"}</dd>
                    </div>
                  </div>
                </div>

                <div>
                  <h4>Tags</h4>
                  <div className="tag-wrap">
                    {selectedModule.tags.map((tag) => (
                      <span key={tag} className="tag">{tag}</span>
                    ))}
                  </div>
                </div>
              </div>
            ) : (
              <p>No module selected.</p>
            )}
          </section>
        </main>
      ) : null}
    </div>
  );
}

export default App;