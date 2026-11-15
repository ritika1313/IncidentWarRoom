import { fmtTime } from "../utils/format.js";
import { Empty } from "./ui.jsx";

const label = (s) => s.replace(/_/g, " ");

export default function Timeline({ events }) {
  if (!events.length) return <Empty>No timeline events.</Empty>;
  return (
    <ol className="relative ml-2 border-l border-slate-700">
      {events.map((e, i) => (
        <li key={i} className="mb-5 ml-5">
          <span className="absolute -left-1.5 mt-1.5 h-3 w-3 rounded-full border-2 border-slate-900 bg-indigo-500" />
          <div className="flex flex-wrap items-baseline gap-x-3">
            <span className="font-medium text-slate-100">{e.agent}</span>
            <span className="text-sm capitalize text-indigo-300">{label(e.event)}</span>
            <span className="text-xs text-slate-500">{fmtTime(e.timestamp)}</span>
          </div>
        </li>
      ))}
    </ol>
  );
}
