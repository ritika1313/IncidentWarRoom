import { useState } from "react";
import { Trash2 } from "lucide-react";
import useIncidents from "../utils/useIncidents.js";
import { removeHistoryId } from "../utils/history.js";
import IncidentRow from "../components/IncidentRow.jsx";
import { PageTitle, Spinner, Empty } from "../components/ui.jsx";

export default function IncidentHistory() {
  const { items, loading } = useIncidents(50);
  const [removed, setRemoved] = useState([]);
  const visible = items.filter((i) => !removed.includes(i.id));

  return (
    <>
      <PageTitle title="Incident History"
        subtitle="The backend has no list endpoint, so this shows incidents created or opened in this browser, loaded via GET /incidents/{id}." />
      {loading ? <Spinner /> : visible.length === 0 ? (
        <Empty>No incidents in this browser yet.</Empty>
      ) : (
        <div className="space-y-3">
          {visible.map((item) => (
            <div key={item.id} className="flex items-stretch gap-2">
              <div className="flex-1"><IncidentRow item={item} /></div>
              {!item.report && (
                <button title="Remove from history" className="rounded-lg border border-slate-800 px-3 text-slate-400 hover:text-red-400"
                  onClick={() => { removeHistoryId(item.id); setRemoved([...removed, item.id]); }}>
                  <Trash2 className="h-4 w-4" />
                </button>
              )}
            </div>
          ))}
        </div>
      )}
    </>
  );
}
