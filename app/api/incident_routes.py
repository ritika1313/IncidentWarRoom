from fastapi import APIRouter, HTTPException

from app.models.incident import IncidentInput
from app.services.incident_workflow import IncidentWorkflow
from app.services.run_logger import load_incident_run

router = APIRouter()

# Temporary in-memory storage for completed incidents
incident_reports = {}


@router.post("/incidents")
async def create_incident(incident: IncidentInput):

    workflow = IncidentWorkflow()

    report = await workflow.run(
        service=incident.service,
        symptom=incident.symptom,
        severity=incident.severity
    )

    incident_id = report["incident"]["incident_id"]

    incident_reports[incident_id] = report

    return {
        "message": "Incident investigated successfully.",
        "incident_id": incident_id,
        "report": report
    }


@router.get("/incidents/{incident_id}")
def get_incident(incident_id: str):

    report = incident_reports.get(incident_id)
    if report is None:
        report = load_incident_run(incident_id)

    if report is None:
        raise HTTPException(
            status_code=404,
            detail="Incident not found."
        )

    return report
