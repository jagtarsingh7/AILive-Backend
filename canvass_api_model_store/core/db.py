"""Module database connection generator."""
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from canvass_api_model_store.core.config import settings

async_engine = create_async_engine(settings.database_url, future=True, echo=settings.debug)


async def get_async_session() -> AsyncSession:
    """Function to get an async session.

    Args:
        No arguments

    Returns:
        An instance of the AsyncSession.

    Raises:
        No Exceptions defined

    """
    async_session = sessionmaker(
        async_engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )

    async with async_session() as session:
        yield session
