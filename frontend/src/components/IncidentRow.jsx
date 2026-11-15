import { Link } from "react-router-dom";
import { fmtTime } from "../utils/format.js";
import { SeverityBadge } from "./ui.jsx";

export default function IncidentRow({ item }) {
  if (!item.report) {
    return (
      <div className="card flex items-center justify-between text-sm text-slate-400">
        <span className="break-all font-mono text-xs">{item.id}</span>
        <span>{item.error === "not-found" ? "Not found on backend" : "Backend unreachable"}</span>
      </div>
    );
  }
  const { incident, decisions } = item.report;
  const decision = (decisions ?? []).at(-1);
  return (
    <Link to={`/incidents/${item.id}`} className="card block transition hover:border-indigo-500/50">
      <div className="flex flex-wrap items-center justify-between gap-2">
        <span className="font-medium text-slate-100">{incident.service}</span>
        <SeverityBadge severity={incident.severity} />
      </div>
      <p className="mt-1 text-sm text-slate-300">{incident.symptom}</p>
      <div className="mt-2 flex flex-wrap items-center justify-between gap-2 text-xs text-slate-500">
        <span>{fmtTime(incident.created_at)}</span>
        <span>{decision ? `Decision: ${decision.action}` : "No decision recorded"}</span>
      </div>
    </Link>
  );
}
