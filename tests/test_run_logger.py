import json

from app.services.run_logger import save_incident_run


def test_run_logger_appends_incident_reports(tmp_path, monkeypatch):

    import app.services.run_logger as logger

    test_log = tmp_path / "incident_runs.jsonl"

    monkeypatch.setattr(logger, "LOG_FILE", test_log)

    first_report = {
        "incident_id": "INC-001",
        "service": "payment service"
    }

    second_report = {
        "incident_id": "INC-002",
        "service": "inventory service"
    }

    save_incident_run(first_report)
    save_incident_run(second_report)

    lines = test_log.read_text(encoding="utf-8").splitlines()

    assert len(lines) == 2
    assert json.loads(lines[0]) == first_report
    assert json.loads(lines[1]) == second_report
