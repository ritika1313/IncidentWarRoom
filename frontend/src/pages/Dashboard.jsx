import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { PlusCircle, CheckCircle2, XCircle } from "lucide-react";
import { getHealth } from "../api/client.js";
import useIncidents from "../utils/useIncidents.js";
import IncidentRow from "../components/IncidentRow.jsx";
import { PageTitle, Spinner, Empty } from "../components/ui.jsx";

export default function Dashboard() {
  const [health, setHealth] = useState({ loading: true });
  const { items, loading } = useIncidents(5);

  useEffect(() => {
    getHealth().then((data) => setHealth({ data })).catch(() => setHealth({ error: true }));
  }, []);

  return (
    <>
      <PageTitle title="Dashboard" subtitle="Overview of the incident response backend and recent investigations.">
        <Link to="/incidents/new" className="btn"><PlusCircle className="h-4 w-4" /> New Incident</Link>
      </PageTitle>

      <div className="mb-6 grid gap-4 sm:grid-cols-2">
        <div className="card">
          <div className="text-sm text-slate-500">Backend</div>
          {health.loading ? <Spinner /> : health.error ? (
            <div className="mt-1 flex items-center gap-2 text-red-400"><XCircle className="h-5 w-5" /> Unreachable</div>
          ) : (
            <div className="mt-1 flex items-center gap-2 text-emerald-400 capitalize">
              <CheckCircle2 className="h-5 w-5" /> {health.data.status}
            </div>
          )}
        </div>
        <div className="card">
          <div className="text-sm text-slate-500">Incidents opened from this browser</div>
          <div className="mt-1 text-2xl font-semibold text-slate-100">{loading ? "…" : items.length}</div>
        </div>
      </div>

      <h2 className="mb-3 font-semibold text-slate-100">Recent incidents</h2>
      {loading ? <Spinner /> : items.length === 0 ? (
        <Empty>No incidents yet. Create one to start an investigation.</Empty>
      ) : (
        <div className="space-y-3">{items.map((it) => <IncidentRow key={it.id} item={it} />)}</div>
      )}
    </>
  );
}
