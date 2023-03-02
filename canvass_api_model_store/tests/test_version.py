"""Module containing function definitions to API version."""
from canvass_api_model_store import __version__


def test_version():
    """Function to test API version.

    Args:
        No arguments

    Asserts:
        Current version of API.

    Raises:
        No Exceptions defined
    """
    assert __version__ == "0.1.0"
