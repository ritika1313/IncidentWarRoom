import { useCallback, useEffect, useState } from "react";
import { RefreshCw, CheckCircle2, XCircle } from "lucide-react";
import { getRoot, getHealth, errorMessage } from "../api/client.js";
import { PageTitle, Spinner } from "../components/ui.jsx";

const ENDPOINTS = [
  { path: "GET /", call: getRoot },
  { path: "GET /health", call: getHealth },
];

export default function BackendHealth() {
  const [results, setResults] = useState({});
  const [loading, setLoading] = useState(true);

  const check = useCallback(async () => {
    setLoading(true);
    const out = {};
    await Promise.all(ENDPOINTS.map(async ({ path, call }) => {
      const start = performance.now();
      try {
        const data = await call();
        out[path] = { ok: true, data, ms: Math.round(performance.now() - start) };
      } catch (err) {
        out[path] = { ok: false, error: errorMessage(err) };
      }
    }));
    setResults(out);
    setLoading(false);
  }, []);

  useEffect(() => { check(); }, [check]);

  return (
    <>
      <PageTitle title="Backend Health" subtitle="Live checks against the FastAPI service.">
        <button className="btn" onClick={check} disabled={loading}><RefreshCw className="h-4 w-4" /> Re-check</button>
      </PageTitle>
      {loading && <Spinner label="Checking…" />}
      <div className="grid gap-4 md:grid-cols-2">
        {ENDPOINTS.map(({ path }) => {
          const r = results[path];
          if (!r) return null;
          return (
            <div key={path} className="card">
              <div className="mb-2 flex items-center justify-between">
                <code className="text-sm text-slate-300">{path}</code>
                {r.ok ? <span className="flex items-center gap-1 text-sm text-emerald-400"><CheckCircle2 className="h-4 w-4" /> OK · {r.ms} ms</span>
                      : <span className="flex items-center gap-1 text-sm text-red-400"><XCircle className="h-4 w-4" /> Failed</span>}
              </div>
              <pre className="overflow-x-auto rounded-lg bg-slate-950 p-3 text-xs text-slate-300">
                {r.ok ? JSON.stringify(r.data, null, 2) : r.error}
              </pre>
            </div>
          );
        })}
      </div>
    </>
  );
}
