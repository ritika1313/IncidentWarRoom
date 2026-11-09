import asyncio

from app.agents.alert_agent import AlertAgent
from app.agents.logs_agent import LogsAgent
from app.agents.dependency_agent import DependencyAgent
from app.agents.mitigation_agent import MitigationAgent
from app.agents.incident_commander import IncidentCommander


def create_test_board():
    board = asyncio.run(
        AlertAgent().process_alert(
            service="Payment Service",
            symptom="Payment API response time increased",
            severity="high"
        )
    )

    asyncio.run(LogsAgent().investigate(board))
    asyncio.run(DependencyAgent().investigate(board))

    return board


def test_commander_records_final_decision():
    board = create_test_board()

    recommendation = asyncio.run(
        MitigationAgent().recommend(board)
    )

    asyncio.run(
        IncidentCommander().make_decision(board, recommendation)
    )

    decisions = board.get_board_state()["decisions"]

