from fastapi import FastAPI

from app.api.incident_routes import router as incident_router

app = FastAPI(
    title="IT Incident Response War-Room",
    description="A multi-agent system for investigating IT incidents.",
    version="1.0.0"
)


@app.get("/")
def home():
    return {
        "message": "IT Incident Response War-Room backend is running!",
        "status": "Success"
    }


@app.get("/health")
def health_check():
    return {
        "project": "IT Incident Response War-Room",
        "status": "healthy"
    }


app.include_router(incident_router)
