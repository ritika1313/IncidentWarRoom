import axios from "axios";

// Requests go to /api/* and are proxied to FastAPI by Vite (see vite.config.js).
// Set VITE_API_BASE_URL to call a CORS-enabled backend directly instead.
const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || "/api",
  timeout: 120000, // POST /incidents runs the whole workflow
});

export const getRoot = () => api.get("/").then((r) => r.data);
export const getHealth = () => api.get("/health").then((r) => r.data);
export const createIncident = (payload) =>
  api.post("/incidents", payload).then((r) => r.data);
export const getIncident = (id) =>
  api.get(`/incidents/${encodeURIComponent(id)}`).then((r) => r.data);

// Turn an axios error into a readable message (FastAPI uses `detail`).
export function errorMessage(err) {
  const detail = err?.response?.data?.detail;
  if (typeof detail === "string") return detail;
  if (Array.isArray(detail))
    return detail.map((d) => `${(d.loc || []).slice(1).join(".")}: ${d.msg}`).join("; ");
  if (err?.response) return `Request failed (HTTP ${err.response.status}).`;
  return "Cannot reach the backend. Is FastAPI running on port 8000?";
}
