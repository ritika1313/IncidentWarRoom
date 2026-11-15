import { Routes, Route, Navigate } from "react-router-dom";
import Layout from "./components/Layout.jsx";
import Dashboard from "./pages/Dashboard.jsx";
import CreateIncident from "./pages/CreateIncident.jsx";
import IncidentDetails from "./pages/IncidentDetails.jsx";
import IncidentHistory from "./pages/IncidentHistory.jsx";
import BackendHealth from "./pages/BackendHealth.jsx";

export default function App() {
  return (
    <Layout>
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/incidents/new" element={<CreateIncident />} />
        <Route path="/incidents/:incidentId" element={<IncidentDetails />} />
        <Route path="/history" element={<IncidentHistory />} />
        <Route path="/health" element={<BackendHealth />} />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </Layout>
  );
}
