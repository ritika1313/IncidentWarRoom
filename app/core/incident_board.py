
from datetime import datetime, timezone
from threading import RLock
from typing import Any

from app.models.incident import (
    IncidentRecord,
    AgentFinding,
    MitigationDecision
)


class IncidentBoard:

    def __init__(self, incident: IncidentRecord):

        # Unique incident information.
        self.incident = incident

        # Findings posted by all agents.
        self.findings: list[AgentFinding] = []

        # Decisions made by Incident Commander.
        self.decisions: list[MitigationDecision] = []

        # Append-only activity timeline.
        self.timeline: list[dict[str, Any]] = []

        # Protect shared state during concurrent access.
        self._lock = RLock()

        # Record initial incident creation.
        self._record_event(
            agent="Alert Agent",
            event="incident_received",
            details={
                "service": incident.service,
                "symptom": incident.symptom,
                "severity": incident.severity
            }
        )

    # Record every activity on the board.
    def _record_event(
        self,
        agent: str,
        event: str,
        details: dict[str, Any]
    ):

        self.timeline.append({
            "agent": agent,
            "event": event,
            "details": details.copy(),
            "timestamp": datetime.now(timezone.utc).isoformat()
        })

    # Allow an agent to read current incident information.
    def get_incident(self):

        with self._lock:
            return self.incident.model_copy(deep=True)

    # Allow an agent to read all available findings.
    def get_findings(self):

        with self._lock:
            return [
                finding.model_copy(deep=True)
                for finding in self.findings
            ]

    # Allow an agent to post its investigation findings.
    def post_finding(self, finding: AgentFinding):

        with self._lock:

            self.findings.append(finding.model_copy(deep=True))

            self._record_event(
                agent=finding.agent,
                event="finding_posted",
                details={
                    "finding_id": finding.finding_id,
                    "finding": finding.finding,
                    "evidence": finding.evidence,
                    "tools_used": finding.tools_used
                }
            )

    # Store the Incident Commander's final decision.
    def post_decision(self, decision: MitigationDecision):

        with self._lock:

            # Verify that all referenced findings exist.
            available_ids = {
                finding.finding_id for finding in self.findings
            }

            if not set(decision.supporting_finding_ids).issubset(
                available_ids
            ):
                raise ValueError(
                    "Decision references findings not present on the board."
                )

            self.decisions.append(decision.model_copy(deep=True))

            self._record_event(
                agent="Incident Commander",
                event="decision_recorded",
                details=decision.model_dump(mode="json")
            )

    # Return a complete snapshot of the board.
    def get_board_state(self):

        with self._lock:

            return {
                "incident": self.incident.model_dump(mode="json"),

                "findings": [
                    finding.model_dump(mode="json")
                    for finding in self.findings
                ],

                "decisions": [
                    decision.model_dump(mode="json")
                    for decision in self.decisions
                ],

                "timeline": [
                    event.copy()
                    for event in self.timeline
                ]
            }
