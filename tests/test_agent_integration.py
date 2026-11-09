import asyncio

from app.services.incident_workflow import IncidentWorkflow


def test_complete_incident_workflow():

    workflow = IncidentWorkflow()

    result = asyncio.run(
        workflow.run(
            service="Payment Service",
            symptom="Payment API response time increased",
            severity="high"
        )
    )

    assert result["incident"]["service"] == "payment service"
    assert len(result["findings"]) == 2
    assert len(result["decisions"]) == 1

    assert result["decisions"][0]["action"] in [
        "rollback", "restart", "failover", "monitor", "escalate"
    ]

    assert len(result["timeline"]) >= 4


def test_workflow_records_all_agent_findings():

    workflow = IncidentWorkflow()

    result = asyncio.run(
        workflow.run(
            service="Payment Service",
            symptom="Payment API failure",
            severity="critical"
        )
    )

    agents = [
        finding["agent"] for finding in result["findings"]
    ]

    assert "Logs Agent" in agents
    assert "Dependency Agent" in agents

    timeline_agents = [
        event["agent"] for event in result["timeline"]
    ]

    assert "Incident Commander" in timeline_agents
