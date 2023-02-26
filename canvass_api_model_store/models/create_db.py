"""Module for creating table in database. To be runned once to initialize tables."""
from database import Base, engine
from models import User, Model, Prediction

Base.metadata.create_all(engine)
