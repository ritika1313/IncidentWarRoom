
from datetime import datetime, timezone
from typing import Literal
from uuid import uuid4

from pydantic import BaseModel, Field


# Input received when a new IT incident is reported.
class IncidentInput(BaseModel):

    service: str = Field(min_length=1, description="Affected service name")

    symptom: str = Field(min_length=1, description="Observed incident symptom")

    severity: Literal["low", "medium", "high", "critical"]


# Complete incident record stored in the Incident Board.
class IncidentRecord(IncidentInput):

    incident_id: str = Field(default_factory=lambda: str(uuid4()))

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )


# Finding submitted by an individual agent.
class AgentFinding(BaseModel):

    finding_id: str = Field(default_factory=lambda: str(uuid4()))

    agent: str

    finding: str

    evidence: list[str] = Field(default_factory=list)

    tools_used: list[str] = Field(default_factory=list)

    timestamp: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )


# Final mitigation decision made by the Incident Commander.
class MitigationDecision(BaseModel):

    action: Literal[
        "rollback",
        "restart",
        "failover",
        "monitor",
        "escalate"
    ]

    likely_cause: str

    reason: str

    supporting_finding_ids: list[str] = Field(default_factory=list)

    timestamp: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
