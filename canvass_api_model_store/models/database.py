"""Module for connecting to database."""

import os

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = os.environ.get("DATABASE_URL")

engine = create_engine(
    DATABASE_URL,
    echo=True,
)

Base = declarative_base()

SessionLocal = sessionmaker(bind=engine)
