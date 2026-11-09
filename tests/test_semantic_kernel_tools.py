import asyncio

from app.agents.alert_agent import AlertAgent
from app.agents.logs_agent import LogsAgent
from app.agents.dependency_agent import DependencyAgent


def test_semantic_kernel_invokes_all_agent_tools():

    async def run_tools():

        # Initialize all three agents and their registered plugins
        alert = AlertAgent()
        logs = LogsAgent()
        dependency = DependencyAgent()

        # Alert Agent - Tool 1
        result1 = await alert.kernel.invoke(
            plugin_name="alert_tools",
            function_name="validate_alert",
            service_name="Payment Service",
            symptom="Payment API failure",
            severity="high"
        )
        assert "successful" in str(result1).lower()

        # Alert Agent - Tool 2
        result2 = await alert.kernel.invoke(
            plugin_name="alert_tools",
            function_name="normalize_alert",
            service_name=" Payment Service ",
            symptom=" API failure ",
            severity=" HIGH "
        )
        assert result2.value["service"] == "payment service"

        # Logs Agent - Tool 1
        result3 = await logs.kernel.invoke(
            plugin_name="logs_tools",
            function_name="search_service_logs",
            service_name="Payment Service"
        )
        logs_text = str(result3.value)
        assert "ERROR" in str(result3)

        # Logs Agent - Tool 2
        result4 = await logs.kernel.invoke(
            plugin_name="logs_tools",
            function_name="analyze_log_errors",
            logs=str(result3)
        )
        assert "error" in str(result4).lower()

        # Dependency Agent - Tool 1
        result5 = await dependency.kernel.invoke(
            plugin_name="dependency_tools",
            function_name="get_service_dependencies",
            service_name="Payment Service"
        )
        dependency_text = str(result5.value)
        assert "authentication service" in str(result5).lower()

        # Dependency Agent - Tool 2
        result6 = await dependency.kernel.invoke(
            plugin_name="dependency_tools",
            function_name="find_impacted_services",
            dependency_data=dependency_text
        )
        assert "downstream" in str(result6).lower()

    asyncio.run(run_tools())
