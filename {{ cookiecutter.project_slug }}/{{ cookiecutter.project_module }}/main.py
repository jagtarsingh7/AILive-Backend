"""Main module that runs that FastAPI server."""
import logging

from {{cookiecutter.project_module}} import __version__
from {{cookiecutter.project_module}}.core.app import create_app
from {{cookiecutter.project_module}}.core.config import settings

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s\t%(asctime)s\t%(message)s",
)

logger = logging.getLogger(__name__)
logger.info(f"{__name__} v{__version__}")

app = create_app()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "{{ cookiecutter.project_module }}.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.debug,
    )
