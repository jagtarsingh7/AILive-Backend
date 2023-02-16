"""Generated file for Alembic."""
import asyncio
from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlmodel import SQLModel

from alembic import context
from alembic.script import ScriptDirectory
from canvass_api_model_store.core.config import settings
from canvass_api_model_store.models import *  # noqa: F401, F403

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)


target_metadata = SQLModel.metadata

target_metadata.naming_convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)" "s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def filter_db_objects(
    object,  # noqa: indirect usage
    name,
    type_,
    *args,  # noqa: indirect usage
    **kwargs,  # noqa: indirect usage
):
    """Filter out database objects that are not part of the models.

    Args:
        object: The object to filter.
        name: The name of the object.
        type_: The type of the object.
        *args: The arguments.
        **kwargs: The keyword arguments.

    Returns:
        True if the object is part of the models, False otherwise.

    Raises:
        No Exceptions defined

    """
    if type_ == "table":
        return name not in settings.exclude_tables

    if type_ == "index" and name.startswith("idx") and name.endswith("geom"):
        return False

    return True


def process_revision_directives(context, revision, directives):
    """Generate sequential revision ids.

    Args:
        context: The context.
        revision: The revision.
        directives: The directives.

    Returns:
        No return value.

    """
    # extract Migration
    migration_script = directives[0]
    # extract current head revision
    head_revision = ScriptDirectory.from_config(context.config).get_current_head()

    if head_revision is None:
        # edge case with first migration
        new_rev_id = 1
    else:
        # default branch with incrementation
        last_rev_id = int(head_revision.lstrip("0"))
        new_rev_id = last_rev_id + 1
    # fill zeros up to 4 digits: 1 -> 0001
    migration_script.rev_id = "{0:04}".format(new_rev_id)


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    Args:
        No arguments

    Returns:
        No return value.

    """
    context.configure(
        url=settings.database_url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        include_object=filter_db_objects,
        process_revision_directives=process_revision_directives,
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    """Run migrations.

    Args:
        connection: The connection.

    Raises:
        No Exceptions defined

    Returns:
        No return value.

    """
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            include_object=filter_db_objects,
            process_revision_directives=process_revision_directives,
        )
        context.run_migrations()


async def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    Args:
        No arguments

    Raises:
        No Exceptions defined

    Returns:
        No return value.

    """
    configuration = config.get_section(config.config_ini_section)
    configuration["sqlalchemy.url"] = settings.database_url
    connectable = AsyncEngine(
        engine_from_config(
            configuration,
            prefix="sqlalchemy.",
            poolclass=pool.NullPool,
            future=True,
        )
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
