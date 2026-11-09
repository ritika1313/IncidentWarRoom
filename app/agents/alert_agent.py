from semantic_kernel import Kernel
from semantic_kernel.functions import kernel_function

from app.models.incident import IncidentRecord
from app.core.incident_board import IncidentBoard


class AlertTools:

    @kernel_function(
        name="validate_alert",
        description="Validate the service, symptom and severity of an incident."
    )
    def validate_alert(self, service_name: str, symptom: str, severity: str) -> str:

        if not service_name.strip():
            raise ValueError("Service name cannot be empty.")

        if not symptom.strip():
            raise ValueError("Incident symptom cannot be empty.")

        allowed_severities = ["low", "medium", "high", "critical"]

        if severity.lower().strip() not in allowed_severities:
            raise ValueError("Invalid severity level.")

        return "Alert validation successful."

    @kernel_function(
        name="normalize_alert",
        description="Clean and standardize incident details."
    )
    def normalize_alert(self, service_name: str, symptom: str, severity: str) -> dict:

        return {
            "service": service_name.strip().lower(),
            "symptom": symptom.strip(),
            "severity": severity.strip().lower()
        }


class AlertAgent:

    def __init__(self, kernel: Kernel = None):
        self.kernel = kernel if kernel is not None else Kernel()
        self.tools = AlertTools()

        self.kernel.add_plugin(
            plugin=self.tools,
            plugin_name="alert_tools"
        )

    async def process_alert(
        self,
        service: str,
        symptom: str,
        severity: str
    ) -> IncidentBoard:

        await self.kernel.invoke(
            plugin_name="alert_tools",
            function_name="validate_alert",
            service_name=service,
            symptom=symptom,
            severity=severity
        )

        result = await self.kernel.invoke(
            plugin_name="alert_tools",
            function_name="normalize_alert",
            service_name=service,
            symptom=symptom,
            severity=severity
        )

        alert_data = result.value

        incident = IncidentRecord(
            service=alert_data["service"],
            symptom=alert_data["symptom"],
            severity=alert_data["severity"]
        )

        board = IncidentBoard(incident)

        print("Alert Agent: Incident received successfully.")
        print("Incident ID:", incident.incident_id)
        print("Service:", incident.service)
        print("Severity:", incident.severity)

        return board
