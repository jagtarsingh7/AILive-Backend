"""Module containing the Models classes."""
# Import all models dynamically to make them available for Alembic
# and for the SQLAlchemy ORM.

import glob
from os.path import basename, dirname, isfile

modules = glob.glob(dirname(__file__) + "/*.py")
__all__ = [basename(f)[:-3] for f in modules if isfile(f) and not f.endswith("__init__.py")]
