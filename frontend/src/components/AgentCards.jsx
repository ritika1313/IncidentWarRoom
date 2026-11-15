import { Bell, FileSearch, Network, Wrench, Gavel } from "lucide-react";
import { fmtTime } from "../utils/format.js";
import { Empty } from "./ui.jsx";

// Shows only what the backend returned for each agent.
function Card({ icon: Icon, name, done, children }) {
  return (
    <div className="card flex flex-col gap-3">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2 font-medium text-slate-100">
          <Icon className="h-4 w-4 text-indigo-400" /> {name}
        </div>
        <span className={`text-xs ${done ? "text-emerald-400" : "text-slate-500"}`}>
          {done ? "Result recorded" : "No result recorded"}
        </span>
      </div>
      {children}
    </div>
  );
}

const Row = ({ label, value }) => (
  <div className="text-sm">
    <span className="text-slate-500">{label}: </span>
    <span className="text-slate-200">{value}</span>
  </div>
);

function FindingBody({ findings }) {
  if (!findings.length) return <Empty>No finding on the board.</Empty>;
  return findings.map((f) => (
    <div key={f.finding_id} className="space-y-2">
      <p className="text-sm text-slate-200">{f.finding}</p>
      {f.evidence?.length > 0 && (
        <ul className="space-y-1 rounded-lg bg-slate-950 p-2 font-mono text-xs text-slate-400">
          {f.evidence.map((e, i) => <li key={i} className="break-words">{e}</li>)}
        </ul>
      )}
      {f.tools_used?.length > 0 && (
        <div className="flex flex-wrap gap-1">
          {f.tools_used.map((t) => (
            <code key={t} className="rounded bg-slate-800 px-1.5 py-0.5 text-xs text-slate-300">{t}</code>
          ))}
        </div>
      )}
      <div className="text-xs text-slate-500">{fmtTime(f.timestamp)}</div>
    </div>
  ));
}

function ActionBody({ item, empty }) {
  if (!item) return <Empty>{empty}</Empty>;
  return (
    <div className="space-y-1.5">
      <Row label="Action" value={<b className="uppercase">{item.action}</b>} />
      <Row label="Likely cause" value={item.likely_cause} />
      <Row label="Reason" value={item.reason} />
      <Row label="Supporting findings" value={item.supporting_finding_ids?.length ?? 0} />
      <div className="text-xs text-slate-500">{fmtTime(item.timestamp)}</div>
    </div>
  );
}

export default function AgentCards({ report }) {
  const alertEvent = report.timeline.find((e) => e.event === "incident_received");
  const recommendation = report.recommendations.at(-1);
  const decision = report.decisions.at(-1);
  const logs = report.findingFor("Logs Agent");
  const deps = report.findingFor("Dependency Agent");

  return (
    <div className="grid gap-4 md:grid-cols-2">
      <Card icon={Bell} name="Alert Agent" done={!!alertEvent}>
        {alertEvent ? (
          <div className="space-y-1.5">
            <Row label="Service" value={alertEvent.details?.service} />
            <Row label="Symptom" value={alertEvent.details?.symptom} />
            <Row label="Severity" value={alertEvent.details?.severity} />
            <div className="text-xs text-slate-500">{fmtTime(alertEvent.timestamp)}</div>
          </div>
        ) : <Empty>No alert event on the timeline.</Empty>}
      </Card>
      <Card icon={FileSearch} name="Logs Agent" done={logs.length > 0}><FindingBody findings={logs} /></Card>
      <Card icon={Network} name="Dependency Agent" done={deps.length > 0}><FindingBody findings={deps} /></Card>
      <Card icon={Wrench} name="Mitigation Agent" done={!!recommendation}>
        <ActionBody item={recommendation} empty="No recommendation stored for this incident (older runs did not record one)." />
      </Card>
      <Card icon={Gavel} name="Incident Commander" done={!!decision}>
        <ActionBody item={decision} empty="No decision recorded." />
      </Card>
    </div>
  );
}
