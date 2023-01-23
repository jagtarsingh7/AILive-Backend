"""Module containing Factories classes to generate test data."""
import sys

import factory
from sqlalchemy.ext.asyncio import AsyncSession


def register_factories(session: AsyncSession) -> None:
    """Register all factories in the session.

    Args:
        session: An instance of the AsyncSession.

    Returns: None
    """
    import inspect

    for _class in inspect.getmembers(sys.modules[__name__], inspect.isclass):
        if issubclass(_class[1], factory.alchemy.SQLAlchemyModelFactory):
            _class[1]._meta.sqlalchemy_session = session  # noqa: access protected member
