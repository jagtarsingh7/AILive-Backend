"""Module containing models for auth tables."""

import datetime as dt

from models.database import Base
from passlib.hash import bcrypt
from sqlalchemy import ARRAY, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship


class User(Base):
    """User Model for table."""

    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True)
    name = Column(String)
    hashed_password = Column(String)

    models = relationship("Model", order_by="Model.id", back_populates="user")

    def verify_password(self, password: str):
        """Verify password for authentication."""
        return bcrypt.verify(password, self.hashed_password)


class Model(Base):
    """MLModel Model for table."""

    __tablename__ = "models"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    pre_model_order = Column(ARRAY(String))
    post_model_order = Column(ARRAY(String))
    predict_function = Column(String)
    storage_options = Column(ARRAY(String))
    container_options = Column(ARRAY(String))
    model_metadata = Column(ARRAY(String))
    model_version = Column(Integer)
    input_features_and_types = Column(ARRAY(String))
    output_names_and_types = Column(ARRAY(String))
    organization_id = Column(Integer)

    user = relationship("User", back_populates="models")
    predictions = relationship("Prediction", order_by="Prediction.id", back_populates="model")


class Prediction(Base):
    """Prediction Model for table."""

    __tablename__ = "predictions"
    id = Column(Integer, primary_key=True)
    model_id = Column(Integer, ForeignKey("models.id"))
    version = Column(Integer)
    input = Column(ARRAY(String))
    output = Column(ARRAY(String))
    timestamp = Column(DateTime, default=dt.datetime.utcnow)

    model = relationship("Model", back_populates="predictions")
