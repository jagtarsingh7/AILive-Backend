"""Module containing router definitions for the FastAPI application."""
from fastapi import APIRouter

from canvass_api_model_store.core.config import settings

v1_router = APIRouter(prefix=f"/{settings.api_v1_str}")
