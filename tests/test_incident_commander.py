import pytest
import asyncio

from app.agents.alert_agent import AlertAgent
from app.agents.logs_agent import LogsAgent
from app.agents.dependency_agent import DependencyAgent
from app.agents.mitigation_agent import MitigationAgent
from app.agents.incident_commander import IncidentCommander


def create_test_board(severity="high"):

    board = asyncio.run(
        AlertAgent().process_alert(
            service="Payment Service",
            symptom="Payment API response time increased",
            severity=severity
        )
    )

    asyncio.run(LogsAgent().investigate(board))
    asyncio.run(DependencyAgent().investigate(board))

    return board


def prepare_recommendation(board):

    asyncio.run(MitigationAgent().recommend(board))


def test_commander_reads_recommendation_from_board():

    board = create_test_board()

    prepare_recommendation(board)

    commander = IncidentCommander()

    asyncio.run(commander.make_decision(board))

    state = board.get_board_state()

    assert len(state["recommendations"]) == 1
    assert len(state["decisions"]) == 1

    assert (
        state["decisions"][0]["action"]
        == state["recommendations"][0]["action"]
    )


def test_commander_records_decision_in_timeline():

    board = create_test_board()

    prepare_recommendation(board)

    commander = IncidentCommander()

    asyncio.run(commander.make_decision(board))

    timeline = board.get_board_state()["timeline"]

    events = [
        event["event"] for event in timeline
    ]

    assert "recommendation_posted" in events
    assert "decision_recorded" in events


def test_commander_handles_missing_recommendation():

    board = create_test_board()

    commander = IncidentCommander()

    # Commander cannot record a decision without a recommendation.
    with pytest.raises(ValueError):
        asyncio.run(commander.make_decision(board))

    state = board.get_board_state()

    assert len(state["decisions"]) == 0
    assert len(state["recommendations"]) == 0