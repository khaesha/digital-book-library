"""
Healthcheck Route
Provides a simple endpoint to check service uptime and health.
"""
from fastapi import APIRouter
from datetime import datetime

router = APIRouter()

# Record the time when the module is loaded (service start)
SERVICE_START_TIME = datetime.utcnow()

@router.get("/healthcheck", tags=["Healthcheck"])
def healthcheck():
    """
    Returns service status and uptime in seconds.
    """
    now = datetime.utcnow()
    uptime = (now - SERVICE_START_TIME).total_seconds()
    return {
        "status": "ok",
        "uptime_seconds": uptime,
        "timestamp": now.isoformat() + "Z"
    }
