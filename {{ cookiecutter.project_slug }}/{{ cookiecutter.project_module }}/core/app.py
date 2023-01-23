"""Module containing function definition to create an instance of a FastAPI application."""
from canvass_fastapi.application import create_application
from canvass_fastapi.dependencies import access_logger
from fastapi import Depends, FastAPI

from {{cookiecutter.project_module}}.api.health import health_router
from {{cookiecutter.project_module}}.api.v1 import v1_router
from {{cookiecutter.project_module}}.core.config import settings


def create_app() -> FastAPI:
    """Function that returns an instance of the FastAPI app.

    Args:
        No arguments

    Returns:
        An instance of the FastAPI class.

    Raises:
        No Exceptions defined

    """
    app: FastAPI = create_application(
        title="{{ cookiecutter.project_name }}",
        description="{{ cookiecutter.project_description }}",
        service_name="{{ cookiecutter.project_slug }}",
        prefix=settings.api_prefix,
        backend_cors_origin=settings.backend_cors_origin,
    )

    app.router.include_router(health_router, dependencies=[Depends(access_logger)])
    app.router.include_router(v1_router, dependencies=[Depends(access_logger)])

    return app
