
from app.agents.alert_agent import AlertAgent
from app.agents.logs_agent import LogsAgent
from app.agents.dependency_agent import DependencyAgent
from app.agents.mitigation_agent import MitigationAgent
from app.agents.incident_commander import IncidentCommander

from app.services.run_logger import save_incident_run


class IncidentWorkflow:

    def __init__(self):
        self.alert_agent = AlertAgent()
        self.logs_agent = LogsAgent()
        self.dependency_agent = DependencyAgent()
        self.mitigation_agent = MitigationAgent()
        self.commander = IncidentCommander()

    async def run(self, service: str, symptom: str, severity: str):

        print("\n========== INCIDENT WORKFLOW STARTED ==========\n")

        # Step 1: Alert Agent creates the shared Incident Board.
        board = await self.alert_agent.process_alert(
            service=service,
            symptom=symptom,
            severity=severity
        )

        # Step 2: Logs Agent investigates and posts findings.
        await self.logs_agent.investigate(board)

        # Step 3: Dependency Agent investigates and posts findings.
        await self.dependency_agent.investigate(board)

        # Step 4: Mitigation Agent analyzes evidence and posts its recommendation.
        await self.mitigation_agent.recommend(board)

        # Step 5: Incident Commander reads the board and records the final decision.
        await self.commander.make_decision(board)

        # Get the complete incident report from the shared board.
        report = board.get_board_state()

        # Save the completed incident report in the append-only run log.
        save_incident_run(report)

        print("\n========== INCIDENT WORKFLOW COMPLETED ==========\n")

        return report
