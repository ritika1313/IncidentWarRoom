export const fmtTime = (iso) =>
  iso ? new Date(iso).toLocaleString(undefined, { dateStyle: "medium", timeStyle: "medium" }) : "—";

export const SEVERITY_STYLES = {
  low: "bg-emerald-500/15 text-emerald-300 border-emerald-500/30",
  medium: "bg-amber-500/15 text-amber-300 border-amber-500/30",
  high: "bg-orange-500/15 text-orange-300 border-orange-500/30",
  critical: "bg-red-500/15 text-red-300 border-red-500/30",
};

// Pull the pieces the UI needs out of a report. Tolerates older logged runs
// that have no `recommendations` key.
export function parseReport(report) {
  const findings = report?.findings ?? [];
  return {
    incident: report?.incident ?? {},
    findings,
    recommendations: report?.recommendations ?? [],
    decisions: report?.decisions ?? [],
    timeline: report?.timeline ?? [],
    findingFor: (agent) => findings.filter((f) => f.agent === agent),
  };
}
