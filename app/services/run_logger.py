import json
from pathlib import Path
from typing import Any


# Project root directory
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Location of the incident run log
LOG_FILE = PROJECT_ROOT / "logs" / "incident_runs.jsonl"


def save_incident_run(report: dict):

    # Create logs directory if it does not exist
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

    # Open file in append mode so old records are preserved
    with LOG_FILE.open("a", encoding="utf-8") as file:

        # Write one complete incident report per line
        file.write(json.dumps(report, ensure_ascii=False) + "\n")

    print("Incident run saved to append-only log.")


def load_incident_run(incident_id: str) -> dict[str, Any] | None:
    if not LOG_FILE.is_file():
        return None

    with LOG_FILE.open("r", encoding="utf-8") as file:
        for line in file:
            report = json.loads(line)
            incident = report.get("incident")
            if (
                isinstance(incident, dict)
                and incident.get("incident_id") == incident_id
            ):
                return report

    return None
