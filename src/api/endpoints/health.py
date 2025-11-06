import logging
import time
from typing import Dict

from fastapi import APIRouter, Depends, HTTPException
from monthly_functions import MonthlyFunctions
from sqlalchemy import text
from sqlalchemy.orm import Session

from core.settings import settings
from core.settings.database import get_session
from schemas.health import HealthSchema

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/health", response_model=HealthSchema)
def health_check() -> Dict:
    """Basic health check endpoint."""
    response = MonthlyFunctions().hola_mundo()
    response = response + " - OK"
    return {"status": response}


@router.get("/health/database")
def database_health_check(session: Session = Depends(get_session)) -> Dict:
    """
    Database health check endpoint.

    Returns:
        Dict: Database health status and connection details
    """
    start_time = time.time()

    try:
        # Test basic connectivity
        result = session.execute(text("SELECT version();"))
        db_version = result.fetchone()[0]

        # Test timezone configuration
        result = session.execute(text("SHOW timezone;"))
        timezone = result.fetchone()[0]

        # Test current timestamp
        result = session.execute(text("SELECT NOW();"))
        current_time = result.fetchone()[0]

        connection_time = time.time() - start_time

        return {
            "status": "healthy",
            "database": {
                "version": db_version,
                "timezone": timezone,
                "current_time": str(current_time),
                "connection_time_ms": round(connection_time * 1000, 2),
            },
            "environment": settings.ENVIRONMENT,
        }

    except Exception as e:
        connection_time = time.time() - start_time
        logger.error(f"Database health check failed: {str(e)}")

        raise HTTPException(
            status_code=503,
            detail={
                "status": "unhealthy",
                "error": str(e),
                "connection_time_ms": round(connection_time * 1000, 2),
                "environment": settings.ENVIRONMENT,
            },
        )
