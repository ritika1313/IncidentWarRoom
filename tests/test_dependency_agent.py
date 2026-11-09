import asyncio

from app.agents.alert_agent import AlertAgent
from app.agents.dependency_agent import DependencyAgent


def create_test_board(service="Payment Service"):
    alert_agent = AlertAgent()

    return asyncio.run(
        alert_agent.process_alert(
            service=service,
            symptom="API response time increased",
            severity="high"
        )
    )


def test_dependency_agent_finds_dependencies():
    board = create_test_board()
    agent = DependencyAgent()

    asyncio.run(agent.investigate(board))

    findings = board.get_findings()

    assert len(findings) == 1
    assert findings[0].agent == "Dependency Agent"
    assert "authentication service" in findings[0].finding.lower()


def test_dependency_agent_handles_unknown_service():
    board = create_test_board("Unknown Service")
    agent = DependencyAgent()

    asyncio.run(agent.investigate(board))

    findings = board.get_findings()

    assert len(findings) == 1
    assert "no dependency information" in findings[0].finding.lower()


def test_dependency_agent_records_tools_used():
    board = create_test_board()
    agent = DependencyAgent()

    asyncio.run(agent.investigate(board))

    finding = board.get_findings()[0]

    assert "get_service_dependencies" in finding.tools_used
    assert "find_impacted_services" in finding.tools_used
