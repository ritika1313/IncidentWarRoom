
import json

from semantic_kernel import Kernel
from semantic_kernel.functions import kernel_function

from app.core.incident_board import IncidentBoard
from app.models.incident import MitigationDecision


class MitigationTools:

    @kernel_function(
        name="analyze_incident_evidence",
        description="Analyze incident findings posted by other agents."
    )
    def analyze_incident_evidence(self, findings_data: str) -> str:

        findings = json.loads(findings_data)

        if not findings:
            return json.dumps({
                "likely_cause": "Insufficient evidence",
                "reason": "No agent findings are available."
            })

        combined_text = " ".join(
            finding["finding"].lower() for finding in findings
        )

        if "database" in combined_text or "connection timeout" in combined_text:
            cause = "Database connectivity issue"
        elif "payment provider" in combined_text or "gateway" in combined_text:
            cause = "Payment provider or gateway issue"
        else:
            cause = "Service-level issue or unknown cause"

        return json.dumps({
            "likely_cause": cause,
            "reason": combined_text
        })

    @kernel_function(
        name="recommend_mitigation",
        description="Recommend a mitigation action based on incident evidence and severity."
    )
    def recommend_mitigation(
        self,
        analysis_data: str,
        severity: str
    ) -> str:

        analysis = json.loads(analysis_data)
        cause = analysis["likely_cause"]

        if cause == "Insufficient evidence":
            action = "escalate"
            reason = "Insufficient evidence is available. Escalation is recommended."

        elif severity.lower() == "critical":
            action = "failover"
            reason = "Critical severity requires switching to a backup service."

        elif cause == "Database connectivity issue":
            action = "restart"
            reason = "A controlled service restart may restore database connectivity."

        elif cause == "Payment provider or gateway issue":
            action = "failover"
            reason = "Switching to an alternative payment route may restore service."

        elif severity.lower() == "high":
            action = "rollback"
            reason = "A rollback may restore the service to its previous stable version."

        else:
            action = "monitor"
            reason = "Continue monitoring while gathering more evidence."

        return json.dumps({
            "action": action,
            "likely_cause": cause,
            "reason": reason
        })


class MitigationAgent:

    def __init__(self, kernel: Kernel = None):
        self.kernel = kernel if kernel is not None else Kernel()
        self.tools = MitigationTools()

        self.kernel.add_plugin(
            plugin=self.tools,
            plugin_name="mitigation_tools"
        )

    async def recommend(self, board: IncidentBoard):

        # Read incident information from the shared board.
        incident = board.get_incident()

        # Read findings posted by Logs and Dependency Agents.
        findings = board.get_findings()

        findings_data = json.dumps([
            {
                "agent": finding.agent,
                "finding": finding.finding,
                "evidence": finding.evidence,
                "finding_id": finding.finding_id
            }
            for finding in findings
        ])

        # Tool 1: Analyze the available incident evidence.
        result1 = await self.kernel.invoke(
            plugin_name="mitigation_tools",
            function_name="analyze_incident_evidence",
            findings_data=findings_data
        )

        analysis_data = str(result1.value)

        # Tool 2: Recommend an appropriate mitigation action.
        result2 = await self.kernel.invoke(
            plugin_name="mitigation_tools",
            function_name="recommend_mitigation",
            analysis_data=analysis_data,
            severity=incident.severity
        )

        recommendation = json.loads(str(result2.value))

        # Create the mitigation decision.
        decision = MitigationDecision(
            action=recommendation["action"],
            likely_cause=recommendation["likely_cause"],
            reason=recommendation["reason"],
            supporting_finding_ids=[
                finding.finding_id for finding in findings
            ]
        )

        # IMPORTANT: Post recommendation to the shared Incident Board.
        board.post_recommendation(decision)

        print("Mitigation Agent: Recommendation posted to Incident Board.")
        print("Recommended action:", decision.action)
        print("Likely cause:", decision.likely_cause)

        return decision
