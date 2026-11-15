import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Play } from "lucide-react";
import { createIncident, errorMessage } from "../api/client.js";
import { addHistoryId } from "../utils/history.js";
import { PageTitle, ErrorBox, Spinner } from "../components/ui.jsx";

const SEVERITIES = ["low", "medium", "high", "critical"];

export default function CreateIncident() {
  const navigate = useNavigate();
  const [form, setForm] = useState({ service: "", symptom: "", severity: "high" });
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");

  const set = (k) => (e) => setForm({ ...form, [k]: e.target.value });

  async function submit(e) {
    e.preventDefault();
    setBusy(true);
    setError("");
    try {
      const data = await createIncident({
        service: form.service.trim(),
        symptom: form.symptom.trim(),
        severity: form.severity,
      });
      addHistoryId(data.incident_id);
      navigate(`/incidents/${data.incident_id}`);
    } catch (err) {
      setError(errorMessage(err));
      setBusy(false);
    }
  }

  return (
    <>
      <PageTitle title="Create Incident" subtitle="Submitting runs the backend investigation workflow." />
      <form onSubmit={submit} className="card max-w-xl space-y-4">
        <label className="block text-sm">
          <span className="mb-1 block text-slate-400">Service</span>
          <input className="input" required value={form.service} onChange={set("service")} placeholder="e.g. payment service" />
        </label>
        <label className="block text-sm">
          <span className="mb-1 block text-slate-400">Symptom</span>
          <textarea className="input" rows={3} required value={form.symptom} onChange={set("symptom")} placeholder="e.g. Database connection timeout" />
        </label>
        <label className="block text-sm">
          <span className="mb-1 block text-slate-400">Severity</span>
          <select className="input capitalize" value={form.severity} onChange={set("severity")}>
            {SEVERITIES.map((s) => <option key={s} value={s}>{s}</option>)}
          </select>
        </label>
        {error && <ErrorBox message={error} />}
        <div className="flex items-center gap-3">
          <button className="btn" disabled={busy || !form.service.trim() || !form.symptom.trim()}>
            <Play className="h-4 w-4" /> Start investigation
          </button>
          {busy && <Spinner label="Investigating…" />}
        </div>
      </form>
    </>
  );
}
