// The backend has no "list incidents" endpoint, so history is the list of
// incident IDs this browser created or opened. Details are always fetched
// from GET /incidents/{id}.
const KEY = "warroom.incident-ids";

export function getHistoryIds() {
  try {
    const ids = JSON.parse(localStorage.getItem(KEY) || "[]");
    return Array.isArray(ids) ? ids : [];
  } catch {
    return [];
  }
}

export function addHistoryId(id) {
  const ids = [id, ...getHistoryIds().filter((x) => x !== id)].slice(0, 50);
  try { localStorage.setItem(KEY, JSON.stringify(ids)); } catch { /* ignore */ }
}

export function removeHistoryId(id) {
  try {
    localStorage.setItem(KEY, JSON.stringify(getHistoryIds().filter((x) => x !== id)));
  } catch { /* ignore */ }
}
