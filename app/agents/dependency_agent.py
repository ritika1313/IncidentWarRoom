import json

from semantic_kernel import Kernel
from semantic_kernel.functions import kernel_function

from app.core.incident_board import IncidentBoard
from app.models.incident import AgentFinding


class DependencyTools:

    SERVICE_DEPENDENCIES = {
        "payment service": {
            "upstream": [
                "authentication service",
                "payment database",
                "payment gateway"
            ],
            "downstream": [
                "order service",
                "billing service"
            ]
        },
        "inventory service": {
            "upstream": [
                "inventory database",
                "warehouse service"
            ],
            "downstream": [
                "order service",
                "product catalog service"
            ]
        },
        "authentication service": {
            "upstream": [
                "user database"
            ],
            "downstream": [
                "payment service",
                "order service"
            ]
        }
    }

    @kernel_function(
        name="get_service_dependencies",
        description="Retrieve upstream and downstream dependencies of a service."
    )
    def get_service_dependencies(self, service_name: str) -> str:

        service_name = service_name.strip().lower()

        dependencies = self.SERVICE_DEPENDENCIES.get(service_name)

        if dependencies is None:
            return json.dumps({
                "service": service_name,
                "upstream": [],
                "downstream": [],
                "found": False
            })

        return json.dumps({
            "service": service_name,
            "upstream": dependencies["upstream"],
            "downstream": dependencies["downstream"],
            "found": True
        })

    @kernel_function(
        name="find_impacted_services",
        description="Identify services that may be impacted by an incident."
    )
    def find_impacted_services(self, dependency_data: str) -> str:

        data = json.loads(dependency_data)

        if not data.get("found"):
            return "No dependency information found for this service."

        upstream = data.get("upstream", [])
        downstream = data.get("downstream", [])

        return (
            f"Upstream dependencies: {', '.join(upstream)}. "
            f"Downstream potentially impacted services: {', '.join(downstream)}."
        )


class DependencyAgent:

    def __init__(self, kernel: Kernel = None):
        self.kernel = kernel if kernel is not None else Kernel()
        self.tools = DependencyTools()

        self.kernel.add_plugin(
            plugin=self.tools,
            plugin_name="dependency_tools"
        )

    async def investigate(self, board: IncidentBoard):

        incident = board.get_incident()

        result1 = await self.kernel.invoke(
            plugin_name="dependency_tools",
            function_name="get_service_dependencies",
            service_name=incident.service
        )

        dependency_data = str(result1.value)

        result2 = await self.kernel.invoke(
            plugin_name="dependency_tools",
            function_name="find_impacted_services",
            dependency_data=dependency_data
        )

        impact_analysis = str(result2.value)
        data = json.loads(dependency_data)

        if data.get("found"):
            evidence = [
                f"Upstream: {', '.join(data['upstream'])}",
                f"Downstream: {', '.join(data['downstream'])}"
            ]
        else:
            evidence = [
                f"No dependency mapping available for {incident.service}."
            ]

        finding = AgentFinding(
            agent="Dependency Agent",
            finding=impact_analysis,
            evidence=evidence,
            tools_used=[
                "get_service_dependencies",
                "find_impacted_services"
            ]
        )

        board.post_finding(finding)

        print("Dependency Agent: Investigation completed.")
        print("Finding:", impact_analysis)

        return board
