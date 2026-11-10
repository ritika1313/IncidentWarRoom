# IT Incident Response War-Room

## 1. Project Overview

IT Incident Response War-Room is a multi-agent system that automates the investigation and response process for IT incidents.

The system uses five specialized agents and a shared Blackboard (Incident Board) architecture. Each agent performs a specific task, shares its findings through the common board, and contributes to the final incident response.

**Technology Stack:** Python, FastAPI, Microsoft Semantic Kernel, Pydantic, Gemini integration, JSONL.

## 2. Agent Roster and Responsibilities

| Agent | Responsibilities | Python Tools |
|---|---|---|
| Alert Agent | Validates and registers incoming incidents | `validate_alert`, `normalize_alert` |
| Logs Agent | Searches service logs and analyzes errors | `search_service_logs`, `analyze_log_errors` |
| Dependency Agent | Identifies upstream and downstream dependencies | `get_service_dependencies`, `find_impacted_services` |
| Mitigation Agent | Analyzes findings and recommends mitigation | `analyze_incident_evidence`, `recommend_mitigation` |
| Incident Commander | Reviews evidence and prepares the final decision | `review_incident_evidence`, `prepare_final_decision` |

Each agent uses a separate Python module and Semantic Kernel plugin tools.

## 3. Architecture and Why It Fits

The project follows the **Blackboard Architecture**.

All agents communicate through a shared `IncidentBoard`, which stores:

- Incident information
- Investigation findings
- Mitigation recommendations
- Final decisions
- Timestamped execution timeline

The architecture fits incident response because multiple specialized agents can contribute evidence to a common board. The Incident Commander reads the posted evidence and recommendation before recording the final decision.

## 4. Workflow

1. Alert Agent receives and validates an incident.
2. Logs Agent investigates service logs and posts findings.
3. Dependency Agent identifies potentially affected services and posts findings.
4. Mitigation Agent analyzes the available evidence and posts a recommendation.
5. Incident Commander reads the shared board and records the final decision.
6. The completed incident report is saved in an append-only JSONL run log.

Supported mitigation actions include rollback, restart, failover, monitor, and escalate.

## 5. Memory and Retrieval

The shared `IncidentBoard` acts as the workflow's common working memory. Agents retrieve incident information and findings from it.

The Logs Agent uses sample log data, while the Dependency Agent uses predefined service dependency mappings. These are local demonstration tools, not live production monitoring integrations.

Completed incident reports are stored in `logs/incident_runs.jsonl` using append-only logging.

## 6. Demo and Testing

**Run the API:**

```bash
uvicorn app.main:app --reload
```

Open the API documentation at:

`http://127.0.0.1:8000/docs`

**Run the automated tests:**

```bash
python -m pytest -v
```

**Run the demonstration notebook:**

`demo/incident_war_room_demo.ipynb`

The notebook demonstrates the complete multi-agent workflow, execution timeline, investigation findings, mitigation recommendation, and final decision.

Three scenarios are covered:

- High-severity incident
- Critical-severity incident
- Unknown-service incident

**Latest test result:** 33 passed.

## 7. Honest Failure Handling

When an unknown service is received, the Logs Agent may find no matching logs and the Dependency Agent may find no dependency information. Instead of inventing evidence, the agents post their findings about missing information. The Mitigation Agent can then recommend monitoring, and the Incident Commander records the final decision based on the shared board.
