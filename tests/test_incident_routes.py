from fastapi.testclient import TestClient

import app.api.incident_routes as incident_routes
import app.services.run_logger as run_logger
from app.main import app
from app.services.run_logger import save_incident_run


def test_get_incident_loads_report_from_log_after_restart(
    tmp_path,
    monkeypatch
):
    incident_id = "incident-123"
    report = {
        "incident": {
            "incident_id": incident_id,
            "service": "payment service"
        },
        "findings": [],
        "decisions": [],
        "timeline": []
    }

    monkeypatch.setattr(
        incident_routes,
        "incident_reports",
        {}
    )
    monkeypatch.setattr(
        run_logger,
        "LOG_FILE",
        tmp_path / "incident_runs.jsonl"
    )
    save_incident_run(report)

    response = TestClient(app).get(f"/incidents/{incident_id}")

    assert response.status_code == 200
    assert response.json() == report


def test_get_incident_returns_404_for_unknown_id(monkeypatch):
    monkeypatch.setattr(incident_routes, "incident_reports", {})

    response = TestClient(app).get("/incidents/unknown-incident")

    assert response.status_code == 404
    assert response.json() == {"detail": "Incident not found."}
