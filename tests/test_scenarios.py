
import asyncio
from unittest import result

from app.services.incident_workflow import IncidentWorkflow


def run_scenario(service, symptom, severity, monkeypatch):

    # Avoid writing test runs into the actual append-only log.
    monkeypatch.setattr(
        "app.services.incident_workflow.save_incident_run",
        lambda report: None
    )

    workflow = IncidentWorkflow()

    return asyncio.run(
        workflow.run(
            service=service,
            symptom=symptom,
            severity=severity
        )
    )


def test_high_severity_incident(monkeypatch):

    result = run_scenario(
        service="Payment Service",
        symptom="Database connection timeout",
        severity="high",
        monkeypatch=monkeypatch
    )

    assert len(result["recommendations"]) == 1
    assert len(result["decisions"]) == 1

    assert result["recommendations"][0]["action"] == "restart"
    assert result["decisions"][0]["action"] == "restart"


def test_critical_severity_incident(monkeypatch):

    result = run_scenario(
        service="Payment Service",
        symptom="Multiple payment requests are failing",
        severity="critical",
        monkeypatch=monkeypatch
    )

    assert len(result["recommendations"]) == 1
    assert len(result["decisions"]) == 1

    assert result["recommendations"][0]["action"] == "failover"
    assert result["decisions"][0]["action"] == "failover"


def test_unknown_service_incident(monkeypatch):

    result = run_scenario(
        service="Unknown Service",
        symptom="API response time is very high",
        severity="medium",
        monkeypatch=monkeypatch
    )

    assert len(result["recommendations"]) == 1
    assert len(result["decisions"]) == 1

    # No investigation findings means escalation is safer.
    assert result["recommendations"][0]["action"] == "monitor"
    assert result["decisions"][0]["action"] == "monitor"
