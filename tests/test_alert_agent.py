import asyncio
import pytest

from semantic_kernel.exceptions import KernelInvokeException
from app.agents.alert_agent import AlertAgent


def test_alert_agent_creates_incident_board():
    agent = AlertAgent()

    board = asyncio.run(
        agent.process_alert(
            service="Payment Service",
            symptom="Payment API response time increased",
            severity="high"
        )
    )

    incident = board.get_incident()

    assert incident.service == "payment service"
    assert incident.symptom == "Payment API response time increased"
    assert incident.severity == "high"


def test_alert_agent_rejects_invalid_severity():
    agent = AlertAgent()

    with pytest.raises(KernelInvokeException):
        asyncio.run(
            agent.process_alert(
                service="Payment Service",
                symptom="API failure",
                severity="urgent"
            )
        )


def test_alert_agent_rejects_empty_service():
    agent = AlertAgent()

    with pytest.raises(KernelInvokeException):
        asyncio.run(
            agent.process_alert(
                service=" ",
                symptom="API failure",
                severity="high"
            )
        )
