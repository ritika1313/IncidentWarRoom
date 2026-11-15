import { Lightbulb, Gavel } from "lucide-react";
import { fmtTime } from "../utils/format.js";
import { Empty } from "./ui.jsx";

function Panel({ icon: Icon, title, item, empty, accent }) {
  return (
    <div className={`card border-l-4 ${accent}`}>
      <h2 className="mb-3 flex items-center gap-2 font-semibold text-slate-100">
        <Icon className="h-4 w-4" /> {title}
      </h2>
      {!item ? <Empty>{empty}</Empty> : (
        <dl className="space-y-3 text-sm">
          <div><dt className="text-slate-500">Action</dt><dd className="text-lg font-semibold uppercase text-slate-100">{item.action}</dd></div>
          <div><dt className="text-slate-500">Likely cause</dt><dd>{item.likely_cause}</dd></div>
          <div><dt className="text-slate-500">Reason</dt><dd>{item.reason}</dd></div>
          <div><dt className="text-slate-500">Supporting finding IDs</dt>
            <dd className="font-mono text-xs text-slate-400">
              {item.supporting_finding_ids?.length ? item.supporting_finding_ids.map((id) => <div key={id} className="break-all">{id}</div>) : "None"}
            </dd></div>
          <div className="text-xs text-slate-500">{fmtTime(item.timestamp)}</div>
        </dl>
      )}
    </div>
  );
}

export const MitigationPanel = ({ recommendation }) => (
  <Panel icon={Lightbulb} title="Mitigation Recommendation" item={recommendation} accent="border-l-amber-500"
    empty="No recommendation stored for this incident (older runs did not record one)." />
);

export const CommanderPanel = ({ decision }) => (
  <Panel icon={Gavel} title="Incident Commander Decision" item={decision} accent="border-l-indigo-500"
    empty="No decision recorded." />
);
