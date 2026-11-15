import { Loader2, AlertTriangle } from "lucide-react";
import { SEVERITY_STYLES } from "../utils/format.js";

export const PageTitle = ({ title, subtitle, children }) => (
  <div className="mb-6 flex flex-wrap items-start justify-between gap-3">
    <div>
      <h1 className="text-2xl font-semibold text-slate-100">{title}</h1>
      {subtitle && <p className="mt-1 text-sm text-slate-400">{subtitle}</p>}
    </div>
    {children}
  </div>
);

export const SeverityBadge = ({ severity }) => (
  <span className={`rounded-full border px-2.5 py-0.5 text-xs font-medium capitalize ${SEVERITY_STYLES[severity] || "border-slate-700 text-slate-300"}`}>
    {severity || "unknown"}
  </span>
);

export const Spinner = ({ label = "Loading…" }) => (
  <div className="flex items-center gap-2 text-sm text-slate-400">
    <Loader2 className="h-4 w-4 animate-spin" /> {label}
  </div>
);

export const ErrorBox = ({ message }) => (
  <div className="flex items-start gap-2 rounded-lg border border-red-500/30 bg-red-500/10 p-3 text-sm text-red-300">
    <AlertTriangle className="mt-0.5 h-4 w-4 shrink-0" /> <span>{message}</span>
  </div>
);

export const Empty = ({ children }) => (
  <div className="rounded-lg border border-dashed border-slate-700 p-6 text-center text-sm text-slate-500">{children}</div>
);
