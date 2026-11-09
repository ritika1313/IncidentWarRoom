import json

from semantic_kernel import Kernel
from semantic_kernel.functions import kernel_function

from app.core.incident_board import IncidentBoard
from app.models.incident import MitigationDecision


class CommanderTools:

    @kernel_function(
        name="review_incident_evidence",
        description="Review incident findings and validate the mitigation recommendation."
    )
    def review_incident_evidence(
        self,
        findings_data: str,
        recommendation_data: str
    ) -> str:

        findings = json.loads(findings_data)
        recommendation = json.loads(recommendation_data)

        if not findings:
            return json.dumps({
                "action": "escalate",
                "likely_cause": "Insufficient evidence",
                "reason": "No findings are available. Escalation is required.",
                "supporting_finding_ids": []
            })

        allowed_actions = [
            "rollback",
            "restart",
            "failover",
            "monitor",
            "escalate"
        ]

        action = recommendation.get("action", "escalate")

        if action not in allowed_actions:
            action = "escalate"

        return json.dumps({
            "action": action,
            "likely_cause": recommendation.get(
                "likely_cause",
                "Unknown cause"
            ),
            "reason": recommendation.get(
                "reason",
                "No reason provided"
            ),
            "supporting_finding_ids": [
                finding["finding_id"] for finding in findings
            ]
        })

    @kernel_function(
        name="prepare_final_decision",
        description="Prepare the final incident decision for recording."
    )
    def prepare_final_decision(self, analysis_data: str) -> str:

        analysis = json.loads(analysis_data)

        return json.dumps({
            "action": analysis["action"],
            "likely_cause": analysis["likely_cause"],
            "reason": analysis["reason"],
            "supporting_finding_ids": analysis["supporting_finding_ids"]
        })


class IncidentCommander:

    def __init__(self, kernel: Kernel = None):
        self.kernel = kernel if kernel is not None else Kernel()
        self.tools = CommanderTools()

        self.kernel.add_plugin(
            plugin=self.tools,
            plugin_name="commander_tools"
        )

    async def make_decision(self, board: IncidentBoard, recommendation):

        findings = board.get_findings()

        findings_data = json.dumps([
            {
                "finding_id": finding.finding_id,
                "agent": finding.agent,
                "finding": finding.finding
            }
            for finding in findings
        ])

        recommendation_data = json.dumps({
            "action": recommendation.action,
            "likely_cause": recommendation.likely_cause,
            "reason": recommendation.reason
        })

        result1 = await self.kernel.invoke(
            plugin_name="commander_tools",
            function_name="review_incident_evidence",
            findings_data=findings_data,
            recommendation_data=recommendation_data
        )

        analysis_data = str(result1.value)

        result2 = await self.kernel.invoke(
            plugin_name="commander_tools",
            function_name="prepare_final_decision",
            analysis_data=analysis_data
        )

        decision_data = json.loads(str(result2.value))

        decision = MitigationDecision(
            action=decision_data["action"],
            likely_cause=decision_data["likely_cause"],
            reason=decision_data["reason"],
            supporting_finding_ids=decision_data["supporting_finding_ids"]
        )

        board.post_decision(decision)

        print("Incident Commander: Final decision recorded.")
        print("Action:", decision.action)
        print("Likely cause:", decision.likely_cause)

        return board
