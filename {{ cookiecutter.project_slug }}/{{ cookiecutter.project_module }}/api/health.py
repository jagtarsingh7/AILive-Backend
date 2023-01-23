"""Module containing health routes defined for this API."""

from fastapi import APIRouter, status

health_router = APIRouter(prefix="/health")


@health_router.get("/liveness", status_code=status.HTTP_200_OK)
def check_liveness():
    """Liveness probe.

    Returns:
        dict showing liveness
    """
    return {"status": "live"}


@health_router.get("/readiness", status_code=status.HTTP_200_OK)
def check_readiness():
    """Readiness probe.

    Returns:
        dict showing readiness
    """
    return {"status": "ready"}
