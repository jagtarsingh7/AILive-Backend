"""Module containing router definitions for the FastAPI application."""
from fastapi import APIRouter

from {{cookiecutter.project_module}}.core.config import settings

v1_router = APIRouter(prefix=f"/{settings.api_v1_str}")
