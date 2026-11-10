
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

        self.incident = incident
        self.findings: list[AgentFinding] = []
        self.recommendations: list[MitigationDecision] = []
        self.decisions: list[MitigationDecision] = []
        self.timeline: list[dict[str, Any]] = []

        self._lock = RLock()

        self._record_event(
            agent="Alert Agent",
            event="incident_received",
            details={
                "service": incident.service,
                "symptom": incident.symptom,
                "severity": incident.severity
            }
        )

    # Record an activity on the timeline.
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

    # Read incident information.
    def get_incident(self):

        with self._lock:
            return self.incident.model_copy(deep=True)

    # Read all investigation findings.
    def get_findings(self):

        with self._lock:
            return [
                finding.model_copy(deep=True)
                for finding in self.findings
            ]

    # Post investigation findings to the board.
    def post_finding(self, finding: AgentFinding):

        with self._lock:

            self.findings.append(
                finding.model_copy(deep=True)
            )

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

    # Post mitigation recommendation to the shared board.
    def post_recommendation(
        self,
        recommendation: MitigationDecision
    ):

        with self._lock:

            available_ids = {
                finding.finding_id
                for finding in self.findings
            }

            if not set(
                recommendation.supporting_finding_ids
            ).issubset(available_ids):

                raise ValueError(
                    "Recommendation references findings not present on the board."
                )

            self.recommendations.append(
                recommendation.model_copy(deep=True)
            )

            self._record_event(
                agent="Mitigation Agent",
                event="recommendation_posted",
                details=recommendation.model_dump(mode="json")
            )

    # Read recommendations from the board.
    def get_recommendations(self):

        with self._lock:
            return [
                recommendation.model_copy(deep=True)
                for recommendation in self.recommendations
            ]

    # Post final decision made by Incident Commander.
    def post_decision(self, decision: MitigationDecision):

        with self._lock:

            # A recommendation must exist before a final decision.
            if not self.recommendations:
                raise ValueError(
                    "Cannot record decision without a mitigation recommendation."
                )

            # Read the latest recommendation from the board.
            recommendation = self.recommendations[-1]

            # Final action must match the posted recommendation.
            if decision.action != recommendation.action:
                raise ValueError(
                    "Final decision does not match the mitigation recommendation."
                )

            # Final cause must match the posted recommendation.
            if decision.likely_cause != recommendation.likely_cause:
                raise ValueError(
                    "Final decision does not match the recommended likely cause."
                )

            # Validate supporting finding IDs.
            available_ids = {
                finding.finding_id
                for finding in self.findings
            }

            if not set(
                decision.supporting_finding_ids
            ).issubset(available_ids):

                raise ValueError(
                    "Decision references findings not present on the board."
                )

            # Store the final decision.
            self.decisions.append(
                decision.model_copy(deep=True)
            )

            self._record_event(
                agent="Incident Commander",
                event="decision_recorded",
                details=decision.model_dump(mode="json")
            )

    # Return complete shared board state.
    def get_board_state(self):

        with self._lock:

            return {
                "incident": self.incident.model_dump(mode="json"),

                "findings": [
                    finding.model_dump(mode="json")
                    for finding in self.findings
                ],

                "recommendations": [
                    recommendation.model_dump(mode="json")
                    for recommendation in self.recommendations
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
