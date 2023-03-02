"""Module for creating table in database. To be runned once to initialize tables."""
from database import engine
from models import Base, User, Model, Prediction

Base.metadata.create_all(engine)
