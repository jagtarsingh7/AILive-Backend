"""Module containing the definition of the Settings class."""
from functools import lru_cache
from api import constants
from pydantic import BaseSettings, validator


class Settings(BaseSettings):
    """Settings class to create an instance of a FastAPI server.

    Attributes:
        api_v1_str: A string for API v1 prefix.
        api_host: A string indicating the API host.
        api_port: An integer indicating the port on which the application runs.
        api_prefix: A string indicating a URL prefix to the API.
        debug: A boolean to indicate if debug mode activate.
        backend_cors_origin: A list of strings representing allowed origins for resource sharing.
        database_url: A string indicating the connection string for the database.
        exclude_tables: A list of strings indicating tables to exclude from migrations.
    """

    api_v1_str: str = "v1"
    api_host: str = "localhost"
    api_port: int = constants.API_PORT
    api_prefix: str | None = None
    debug: bool = False
    backend_cors_origin: str | list[str] = []
    database_url: str
    exclude_tables: list[str] = []

    @validator("api_prefix", pre=True)
    def assemble_api_prefix(cls, v: str | None) -> str | None:
        """Function that returns an instance of the FastAPI app.

        Args:
            v - parameter to indicate the current API version in the prefix.

        Returns:
            A string indicating the API prefix.

        Raises:
            No Exceptions defined

        """
        if not v or not (root_path := v.strip("/")):
            return None
        return f"/{root_path}"

    @validator("backend_cors_origin", pre=True)
    def assemble_cors_origins(cls, v: str | list[str]) -> list[str] | str:
        """Function that assembles a list of accepted backend CORS origins.

        Args:
            v - list of strings indicating accepted backend CORS origins

        Returns:
            A JSON-formatted list of origins

        Raises:
            ValueError

        """
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)


@lru_cache()
def get_settings():
    """Function that returns an instance of the Settings class.

    Args:
        No arguments

    Returns:
        An instance of the Settings class.

    Raises:
        No Exceptions defined

    """
    return Settings()


settings = get_settings()
