
import pytest

from app.models.incident import (
    IncidentInput,
    IncidentRecord,
    AgentFinding,
    MitigationDecision
)

from app.core.incident_board import IncidentBoard


def create_test_board():

    incident_input = IncidentInput(
        service="Payment Service",
        symptom="Payment requests are timing out",
        severity="critical"
    )

    incident = IncidentRecord(**incident_input.model_dump())

    return IncidentBoard(incident)


def test_incident_creation():

    board = create_test_board()

    state = board.get_board_state()

    assert state["incident"]["service"] == "Payment Service"
    assert state["incident"]["severity"] == "critical"


def test_agent_can_post_finding():

    board = create_test_board()

    finding = AgentFinding(
        agent="Logs Agent",
        finding="Database connection timeout detected",
        evidence=["Connection timeout in payment logs"],
        tools_used=["search_logs", "count_errors"]
    )

    board.post_finding(finding)

    assert len(board.get_findings()) == 1


def test_commander_can_post_decision():

    board = create_test_board()

    finding = AgentFinding(
        agent="Logs Agent",
        finding="Repeated database connection failures",
        evidence=["Database connection timeout"],
        tools_used=["search_logs", "count_errors"]
    )

    board.post_finding(finding)

    decision = MitigationDecision(
        action="restart",
        likely_cause="Database connection failure",
        reason="Logs show repeated connection failures.",
        supporting_finding_ids=[finding.finding_id]
    )

    board.post_decision(decision)

    state = board.get_board_state()

    assert len(state["decisions"]) == 1
    assert state["decisions"][0]["action"] == "restart"


def test_commander_cannot_reference_unknown_finding():

    board = create_test_board()

    decision = MitigationDecision(
        action="restart",
        likely_cause="Unknown",
        reason="Testing invalid evidence reference",
        supporting_finding_ids=["unknown-finding-id"]
    )

    with pytest.raises(ValueError):
        board.post_decision(decision)


def test_timeline_records_activities():

    board = create_test_board()

    finding = AgentFinding(
        agent="Alert Agent",
        finding="High severity incident received",
        evidence=["Critical alert received"],
        tools_used=["validate_alert", "normalize_alert"]
    )

    board.post_finding(finding)

    state = board.get_board_state()

    assert len(state["timeline"]) == 2
    assert state["timeline"][0]["event"] == "incident_received"
    assert state["timeline"][1]["event"] == "finding_posted"
