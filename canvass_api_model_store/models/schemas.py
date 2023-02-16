"""Module containing schemas for auth models."""

import datetime as dt
from typing import Optional

import models.models as _models
from pydantic import BaseModel


class UserBase(BaseModel):
    """BaseModel for User."""

    email: str
    name: str


class UserCreate(UserBase):
    """UserCreate Schema for new Users."""

    hashed_password: str

    class Config:
        """Config for ORM mode."""

        orm_mode = True


class User(UserBase):
    """User Schema for new Users."""

    id: Optional[int] = None

    class Config:
        """Config for ORM mode."""

        orm_mode = True


class ModelBase(BaseModel):
    """BaseModel Schema for Model."""

    pre_model_order: str
    post_model_order: str
    predict_function: str
    storage_options: str
    container_options: str
    model_metadata: str
    version: int
    input_features_and_types: str
    output_names_and_types: str
    organization_id: int


class ModelCreate(ModelBase):
    """ModelCreate Schema for new Model."""

    user_id: int

    class Config:
        """Config for ORM mode."""

        orm_mode = True


class Model(ModelBase):
    """Model Schema for new Model."""

    id: int
    user_id: int

    class Config:
        """Config for ORM mode."""

        orm_mode = True


class PredictionBase(BaseModel):
    """BaseModel Schema for Prediction."""

    model_id: int
    version: int
    input: str
    output: str


class PredictionCreate(PredictionBase):
    """PredictionCreate Schema for new Prediction."""

    timestamp: dt.datetime = dt.datetime.utcnow()

    class Config:
        """Config for ORM mode."""

        orm_mode = True


class Prediction(PredictionBase):
    """Prediction Schema for new Prediction."""

    id: int
    timestamp: dt.datetime

    class Config:
        """Config for ORM mode."""

        orm_mode = True
