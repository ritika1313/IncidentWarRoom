
from semantic_kernel import Kernel
from semantic_kernel.functions import kernel_function

from app.core.incident_board import IncidentBoard
from app.models.incident import AgentFinding


class LogsTools:
    """Tools used by the Logs Agent."""

    # Sample logs for demonstrating log investigation.
    # Later, these can be replaced with real application log files.
    SAMPLE_LOGS = {
        "payment service": [
            "2026-11-09 09:10:00 INFO Payment service started",
            "2026-11-09 09:12:00 ERROR Database connection timeout",
            "2026-11-09 09:13:00 ERROR Payment provider request timed out",
            "2026-11-09 09:14:00 WARN Payment response time exceeded threshold"
        ],
        "inventory service": [
            "2026-11-09 09:10:00 INFO Inventory service started",
            "2026-11-09 09:12:00 WARN Inventory database response is slow",
            "2026-11-09 09:13:00 ERROR Inventory database connection failed"
        ]
    }

    @kernel_function(
        name="search_service_logs",
        description="Search recent logs for the affected service."
    )
    def search_service_logs(self, service_name: str) -> str:

        # Normalize the service name for searching
        service_name = service_name.strip().lower()

        # Retrieve logs for the requested service
        logs = self.SAMPLE_LOGS.get(service_name, [])

        if not logs:
            return "NO_LOGS_FOUND"

        return "\n".join(logs)

    @kernel_function(
        name="analyze_log_errors",
        description="Analyze logs and identify errors and warnings."
    )
    def analyze_log_errors(self, logs: str) -> str:

        # Handle the case where no logs were found
        if not logs.strip() or logs == "NO_LOGS_FOUND":
            return "No matching service logs were found."

        log_entries = logs.splitlines()

        # Identify error and critical entries
        errors = [
            line for line in log_entries
            if " ERROR " in line.upper()
            or " CRITICAL " in line.upper()
        ]

        # Identify warning entries
        warnings = [
            line for line in log_entries
            if " WARN " in line.upper()
            or " WARNING " in line.upper()
        ]

        if errors:
            return (
                f"Detected {len(errors)} error(s) and "
                f"{len(warnings)} warning(s). "
                f"First error: {errors[0]}"
            )

        if warnings:
            return (
                f"No errors detected. "
                f"Detected {len(warnings)} warning(s)."
            )

        return "No errors or warnings detected in the logs."


class LogsAgent:

    def __init__(self, kernel: Kernel = None):

        # Use the supplied Semantic Kernel or create one
        self.kernel = kernel if kernel is not None else Kernel()

        # Initialize the agent's Python tools
        self.tools = LogsTools()

        # Register both tools as a Semantic Kernel plugin
        self.kernel.add_plugin(
            plugin=self.tools,
            plugin_name="logs_tools"
        )

    

    async def investigate(self, board: IncidentBoard):

        # Read incident details from the shared board
        incident = board.get_incident()

        # Tool 1: Search service logs through Semantic Kernel
        result1 = await self.kernel.invoke(
            plugin_name="logs_tools",
            function_name="search_service_logs",
            service_name=incident.service
        )

        logs = str(result1.value)

        # Tool 2: Analyze logs through Semantic Kernel
        result2 = await self.kernel.invoke(
            plugin_name="logs_tools",
            function_name="analyze_log_errors",
            logs=logs
        )

        analysis = str(result2.value)

        # Prepare evidence from the logs
        evidence = (
            ["No matching sample logs were found."]
            if logs == "NO_LOGS_FOUND"
            else logs.splitlines()
        )

        # Create finding
        finding = AgentFinding(
            agent="Logs Agent",
            finding=analysis,
            evidence=evidence,
            tools_used=[
                "search_service_logs",
                "analyze_log_errors"
            ]
        )

        # Post finding to shared Incident Board
        board.post_finding(finding)

        print("Logs Agent: Investigation completed.")
        print("Finding:", analysis)

        return board
