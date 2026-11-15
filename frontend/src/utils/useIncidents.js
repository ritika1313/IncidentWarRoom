import { useEffect, useState } from "react";
import { getIncident } from "../api/client.js";
import { getHistoryIds } from "./history.js";

// Fetches every remembered incident ID from GET /incidents/{id}.
// Returns { items: [{id, report?, error?}], loading }.
export default function useIncidents(limit) {
  const [state, setState] = useState({ items: [], loading: true });

  useEffect(() => {
    let cancelled = false;
    const ids = getHistoryIds().slice(0, limit);
    Promise.allSettled(ids.map((id) => getIncident(id))).then((results) => {
      if (cancelled) return;
      setState({
        loading: false,
        items: results.map((r, i) =>
          r.status === "fulfilled"
            ? { id: ids[i], report: r.value }
            : { id: ids[i], error: r.reason?.response?.status === 404 ? "not-found" : "unreachable" }
        ),
      });
    });
    return () => { cancelled = true; };
  }, [limit]);

  return state;
}
