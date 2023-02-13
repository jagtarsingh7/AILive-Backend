"""Module for connecting to database."""

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

engine = create_engine("postgresql+psycopg2://postgres:capstone@db/api_model_store", echo=True)

Base = declarative_base()

SessionLocal = sessionmaker(bind=engine)
