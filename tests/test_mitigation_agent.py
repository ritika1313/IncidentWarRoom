
import asyncio

from app.agents.alert_agent import AlertAgent
from app.agents.logs_agent import LogsAgent
from app.agents.dependency_agent import DependencyAgent
from app.agents.mitigation_agent import MitigationAgent


def create_test_board(severity="high"):

    alert_agent = AlertAgent()

    board = asyncio.run(
        alert_agent.process_alert(
            service="Payment Service",
            symptom="Payment API response time increased",
            severity=severity
        )
    )

    asyncio.run(LogsAgent().investigate(board))
    asyncio.run(DependencyAgent().investigate(board))

    return board


def test_mitigation_agent_recommends_action():

    board = create_test_board()
    agent = MitigationAgent()

    decision = asyncio.run(agent.recommend(board))

    assert decision.action in [
        "rollback", "restart", "failover", "monitor", "escalate"
    ]

    assert decision.likely_cause != ""


def test_mitigation_agent_uses_board_evidence():

    board = create_test_board()
    agent = MitigationAgent()

    decision = asyncio.run(agent.recommend(board))

    finding_ids = {
        finding.finding_id for finding in board.get_findings()
    }

    assert set(decision.supporting_finding_ids) == finding_ids


def test_critical_incident_recommends_failover():

    board = create_test_board(severity="critical")
    agent = MitigationAgent()

    decision = asyncio.run(agent.recommend(board))

    assert decision.action == "failover"


def test_mitigation_agent_posts_recommendation_to_board():

    board = create_test_board()
    agent = MitigationAgent()

    decision = asyncio.run(agent.recommend(board))

    recommendations = board.get_recommendations()

    assert len(recommendations) == 1
    assert recommendations[0].action == decision.action
    assert recommendations[0].likely_cause == decision.likely_cause
