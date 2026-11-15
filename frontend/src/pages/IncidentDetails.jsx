import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { ArrowLeft } from "lucide-react";
import { getIncident, errorMessage } from "../api/client.js";
import { addHistoryId } from "../utils/history.js";
import { fmtTime, parseReport } from "../utils/format.js";
import { PageTitle, SeverityBadge, Spinner, ErrorBox } from "../components/ui.jsx";
import AgentCards from "../components/AgentCards.jsx";
import Timeline from "../components/Timeline.jsx";
import { MitigationPanel, CommanderPanel } from "../components/DecisionPanels.jsx";

export default function IncidentDetails() {
  const { incidentId } = useParams();
  const [state, setState] = useState({ loading: true });

  useEffect(() => {
    setState({ loading: true });
    getIncident(incidentId)
      .then((report) => {
        addHistoryId(incidentId);
        setState({ report: parseReport(report) });
      })
      .catch((err) => setState({ error: errorMessage(err) }));
  }, [incidentId]);

  if (state.loading) return <Spinner label="Loading incident…" />;
  if (state.error) {
    return (
      <>
        <ErrorBox message={state.error} />
        <Link to="/history" className="mt-4 inline-flex items-center gap-1 text-sm text-indigo-400"><ArrowLeft className="h-4 w-4" /> Back to history</Link>
      </>
    );
  }

  const { report } = state;
  const { incident } = report;

  return (
    <>
      <PageTitle title="Incident Investigation" subtitle={incident.incident_id}>
        <SeverityBadge severity={incident.severity} />
      </PageTitle>

      <div className="card mb-6 grid gap-3 text-sm sm:grid-cols-3">
        <div><div className="text-slate-500">Service</div>{incident.service}</div>
        <div><div className="text-slate-500">Symptom</div>{incident.symptom}</div>
        <div><div className="text-slate-500">Created</div>{fmtTime(incident.created_at)}</div>
      </div>

      <div className="mb-6 grid gap-4 lg:grid-cols-2">
        <MitigationPanel recommendation={report.recommendations.at(-1)} />
        <CommanderPanel decision={report.decisions.at(-1)} />
      </div>

      <h2 className="mb-3 font-semibold text-slate-100">Agent results</h2>
      <div className="mb-6"><AgentCards report={report} /></div>

      <h2 className="mb-3 font-semibold text-slate-100">Incident timeline</h2>
      <div className="card"><Timeline events={report.timeline} /></div>
    </>
  );
}
