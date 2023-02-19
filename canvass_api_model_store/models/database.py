"""Module for connecting to database."""

import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://adminpostgres:MyApass%401@dev-cacn-humbercapstonedb01-psql.postgres.database.azure.com:5432/api_model_store?sslmode=require"

engine = create_engine(
    DATABASE_URL,
    echo=True,
)

SessionLocal = sessionmaker(bind=engine)
