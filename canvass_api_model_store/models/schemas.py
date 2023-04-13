"""Module containing schemas for auth models."""

import datetime as dt
from fastapi import FastAPI, File, UploadFile
from typing import Any, Dict, List, Optional

from pydantic import BaseModel


class UserBase(BaseModel):
    """BaseModel for User.

    Attributes:
        email (str): Email of the user.
        name (str): Name of the user.
        organization (str): Name of user's organization.
    """

    email: str
    name: str
    org: str


class UserCreate(UserBase):
    """UserCreate Schema for new Users.

    Attributes:
        hashed_password (str): Hashed password for the user.

    Configurations:
        orm_mode (bool): Enables ORM mode for this schema.
    """

    hashed_password: str

    class Config:
        """Config for ORM mode."""

        orm_mode = True


class User(UserBase):
    """User Schema for new Users.

    Attributes:
        id (int, optional): User ID.

    Configurations:
        orm_mode (bool): Enables ORM mode for this schema.
    """

    id: Optional[int] = None

    class Config:
        """Config for ORM mode."""

        orm_mode = True


class ModelBase(BaseModel):
    """BaseModel Schema for Model.

    Attributes:
        tags (str): Comma separated list of tags for the model.
        custom_functions (Dict[str, Any]): Dictionary of custom functions for the model.
        pre_model_order (List[str]): List of pre-model order.
        post_model_order (List[str]): List of post-model order.
        predict_function (str): Name of the predict function.
        storage_options (Dict[str, str]): Dictionary of storage options for the model.
        container_options (Dict[str, str]): Dictionary of container options for the model.
        model_metadata (Dict[Any, Any]): Dictionary of model metadata.
        model_version (int): Model version.
        input_features_and_types (Dict[str, str]): Dictionary of input features and their types.
        output_names_and_types (Dict[str, str]): Dictionary of output names and their types.
    """

    tags: str
    # custom_functions:  Dict[str, str]
    pre_model_order: List[str]
    post_model_order: List[str]
    predict_function: str
    # storage_options: Dict[str, str]
    # container_options: Dict[str, str]
    # model_metadata: Dict[Any, Any]
    model_version: int
    # input_features_and_types: Dict[str, str]
    # output_names_and_types: Dict[str, str]


class ModelUpload(ModelBase):
    """ModelUpload Schema for uploading Model."""

    model_file: UploadFile 


class ModelCreate(ModelBase):
    """ModelCreate Schema for new Model.

    Configurations:
        orm_mode (bool): Enables ORM mode for this schema.
    """

    pass


class Model(ModelBase):
    """Model Schema for new Model.

    Attributes:
        id (int): Model ID.
        user_id (int): User ID who created the model.

    Configurations:
        orm_mode (bool): Enables ORM mode for this schema.
    """

    id: int
    user_id: int

    class Config:
        """Config for ORM mode."""

        orm_mode = True


class ModelUpdate(BaseModel):
    """ModelUpdate Schema for updating Model.

    Attributes:
        tags (Optional[str]): Comma separated list of tags for the model.
        custom_functions (Optional[Dict[str, Any]]): Dictionary of custom functions for the model.
        pre_model_order (Optional[List[str]]): List of pre-model order.
        post_model_order (Optional[List[str]]): List of post-model order.
        predict_function (Optional[str]): Name of the predict function.
        storage_options (Optional[Dict[str, str]]): Dictionary of storage options for the model.
        container_options (Optional[Dict[str, str]]): Dictionary of container options for the model.
        model_metadata (Optional[Dict[Any, Any]]): Dictionary of model metadata.
        input_features_and_types (Optional[Dict[str, str]]): Dictionary of input features and their types.
        output_names_and_types (Optional[Dict[str, str]]): Dictionary of output names and their types.
    """

    tags: Optional[str] = None
    custom_functions: Optional[Dict[str, Any]] = None
    pre_model_order: Optional[List[str]] = None
    post_model_order: Optional[List[str]] = None
    predict_function: Optional[str] = None
    storage_options: Optional[Dict[str, str]] = None
    container_options: Optional[Dict[str, str]] = None
    model_metadata: Optional[Dict[Any, Any]] = None
    input_features_and_types: Optional[Dict[str, str]] = None
    output_names_and_types: Optional[Dict[str, str]] = None


class PredictionBase(BaseModel):
    """BaseModel Schema for Prediction.

    Attributes:
        model_id (int): Model ID for the prediction.
        version (int): Model version for the prediction.
        input (Dict[str, Any]): Input data for the prediction.
        output (Dict[str, Any]): Output data from the prediction.
    """

    model_id: int
    version: int
    input: Dict[str, Any]
    output: Dict[str, Any]


class PredictionCreate(PredictionBase):
    """PredictionCreate Schema for new Prediction.

    Attributes:
        timestamp (dt.datetime): Timestamp of the prediction.

    Configurations:
        orm_mode (bool): Enables ORM mode for this schema.
    """

    timestamp: dt.datetime = dt.datetime.utcnow()

    class Config:
        """Config for ORM mode."""

        orm_mode = True


class Prediction(PredictionBase):
    """Prediction Schema for new Prediction.

    Attributes:
        id (int): ID of the prediction.
        timestamp (datetime.datetime): Timestamp of the prediction creation.

    Configurations:
        orm_mode (bool): Enables ORM mode for this schema.
    """

    id: int
    timestamp: dt.datetime

    class Config:
        """Config for ORM mode."""

        orm_mode = True
