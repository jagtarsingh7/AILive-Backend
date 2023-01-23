"""Module containing fixture function definitions used by test suite."""
import pytest
from canvass_fastapi.models import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from {{cookiecutter.project_module}}.core.db import async_engine
from {{cookiecutter.project_module}}.models import *  # noqa: F401, F403
from {{cookiecutter.project_module}}.tests.factories import register_factories


@pytest.fixture(scope="module")
def app():
    """Function that creates a FastAPI app used by the test suite.

    Args:
        No arguments

    Returns:
        An instance of the FastAPI app.

    Raises:
        No Exceptions defined

    """
    from {{cookiecutter.project_module}}.core.app import create_app

    return create_app()


@pytest.fixture(scope="module")
def client(app):
    """A test client for the FastAPI app.

    Args:
        app - An instance of the FastAPI app

    Yields:
        An instance of the FastAPI TestClient.

    Raises:
        No Exceptions defined

    """
    from fastapi.testclient import TestClient

    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="session")
def engine():
    """Create a test database engine.

    Args:
        No arguments

    Yields:
        An instance of the AsyncEngine.

    Raises:
        No Exceptions defined

    """
    yield async_engine
    async_engine.sync_engine.dispose()


@pytest.fixture(autouse=True)
async def create(engine):
    """Create all tables in the database.

    Args:
        engine - An instance of the AsyncEngine.

    Yields:
        No return value.

    Raises:
        No Exceptions defined

    """
    async with engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.drop_all)


@pytest.fixture
async def session(engine):
    """Create a new database session for a test.

    Args:
        engine - An instance of the AsyncEngine.

    Yields:
        An instance of the AsyncSession.

    Raises:
        No Exceptions defined

    """
    async with AsyncSession(engine) as session:
        register_factories(session)
        yield session
