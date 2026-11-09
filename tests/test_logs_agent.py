import asyncio

from app.agents.alert_agent import AlertAgent
from app.agents.logs_agent import LogsAgent


def create_test_board(service="Payment Service"):
    alert_agent = AlertAgent()

    board = asyncio.run(
        alert_agent.process_alert(
            service=service,
            symptom="API response time increased",
            severity="high"
        )
    )
    return board


def test_logs_agent_finds_service_errors():
    board = create_test_board()
    logs_agent = LogsAgent()

    asyncio.run(logs_agent.investigate(board))

    findings = board.get_findings()
    assert len(findings) == 1
    assert findings[0].agent == "Logs Agent"
    assert "error" in findings[0].finding.lower()


def test_logs_agent_handles_missing_logs():
    board = create_test_board("Unknown Service")
    logs_agent = LogsAgent()

    asyncio.run(logs_agent.investigate(board))

    findings = board.get_findings()
    assert len(findings) == 1
    assert "no matching" in findings[0].finding.lower()


def test_logs_agent_records_tools_used():
    board = create_test_board()
    logs_agent = LogsAgent()

    asyncio.run(logs_agent.investigate(board))

    finding = board.get_findings()[0]
    assert "search_service_logs" in finding.tools_used
    assert "analyze_log_errors" in finding.tools_used
