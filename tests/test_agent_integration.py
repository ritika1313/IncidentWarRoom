
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

    # Both investigation agents should post findings.
    assert len(result["findings"]) == 2

    # Mitigation Agent should post a recommendation.
    assert len(result["recommendations"]) == 1

    # Incident Commander should record a final decision.
    assert len(result["decisions"]) == 1

    # Final decision must match the recommendation.
    assert (
        result["decisions"][0]["action"]
        == result["recommendations"][0]["action"]
    )

    assert result["decisions"][0]["action"] in [
        "rollback", "restart", "failover", "monitor", "escalate"
    ]

    assert len(result["timeline"]) >= 5


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

    assert "Alert Agent" in timeline_agents
    assert "Logs Agent" in timeline_agents
    assert "Dependency Agent" in timeline_agents
    assert "Mitigation Agent" in timeline_agents
    assert "Incident Commander" in timeline_agents

    assert len(result["recommendations"]) == 1
    assert len(result["decisions"]) == 1
