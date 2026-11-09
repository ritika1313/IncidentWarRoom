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

        board = await self.alert_agent.process_alert(
            service=service,
            symptom=symptom,
            severity=severity
        )

        await self.logs_agent.investigate(board)
        await self.dependency_agent.investigate(board)

        recommendation = await self.mitigation_agent.recommend(board)

        await self.commander.make_decision(board, recommendation)

        report = board.get_board_state()

        # Save the completed incident report
        save_incident_run(report)

        print("\n========== INCIDENT WORKFLOW COMPLETED ==========\n")

        return report
