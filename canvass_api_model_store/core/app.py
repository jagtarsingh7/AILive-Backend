"""Module containing function definition to create an instance of a FastAPI application."""
from fastapi import FastAPI

from canvass_api_model_store.api.auth import auth_router
from canvass_api_model_store.api.health import health_router
from canvass_api_model_store.api.model import model_router
from canvass_api_model_store.api.v1 import v1_router
from canvass_api_model_store.core.config import settings


def create_app() -> FastAPI:
    """Function that returns an instance of the FastAPI app.

    Args:
        No arguments

    Returns:
        An instance of the FastAPI class.

    Raises:
        No Exceptions defined

    """
    app: FastAPI = FastAPI(
        title="canvass-api-model-store",
        description="FastAPI backend for Canvass AI Live",
        service_name="canvass-api-model-store",
        prefix=settings.api_prefix,
        backend_cors_origin=settings.backend_cors_origin,
    )

    app.router.include_router(health_router)
    app.router.include_router(v1_router)
    app.router.include_router(auth_router)
    app.router.include_router(model_router)

    return app
