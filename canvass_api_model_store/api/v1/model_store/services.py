"""Module containing services for auth routes.

This module provides functions for creating a new model, selecting, updating,
retrieving and deleting a model.

Functions:
    create_model: Function to create a new model.
    model_selector: Function to select a model.
    delete_model: Function to delete a model.

Attributes:
    oauth2schema: OAuth2PasswordBearer object for token authentication.
    JWT_SECRET: Secret key for JSON Web Token authentication.
    TOKEN_TYPE: Token type for JSON Web Token authentication.
"""

import os

import models.models as _models
import models.schemas as _schemas
from fastapi import HTTPException, security, status
from sqlalchemy import orm

oauth2schema = security.OAuth2PasswordBearer(tokenUrl="/auth/api/token")

JWT_SECRET = os.environ.get("JWT_SECRET")
TOKEN_TYPE = os.environ.get("TOKEN_TYPE")


async def create_model(user: _schemas.User, db: orm.Session, model: _schemas.ModelCreate):
    """Function to create new model.

    Args:
        user (_schemas.User): The user object.
        db (orm.Session): SQLAlchemy database session object.
        model (_schemas.ModelCreate): The model to be created.

    Returns:
        The created model object.

    """
    model = _models.Model(**model.dict(), user_id=user.id)
    db.add(model)
    db.commit()
    db.refresh(model)

    return _schemas.Model.from_orm(model)


async def model_selector(model_id: int, user: _schemas.User, db: orm.Session):
    """
    Function to select a model.

    Args:
        model_id (int): The ID of the model to be selected.
        user (_schemas.User): The user object.
        db (orm.Session): SQLAlchemy database session object.

    Returns:
        The selected model object.

    Raises:
        HTTPException: If the model does not exist.
    """
    model = (
        db.query(_models.Model)
        .filter_by(user_id=user.id)
        .filter(_models.Model.id == model_id)
        .one_or_none()
    )

    if model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Model does not exist")

    return model


async def delete_model(model_id: int, user: _schemas.User, db: orm.Session):
    """Deletes a model from the database for a given user.

    Args:
        model_id (int): The id of the model to be deleted.
        user (_schemas.User): The user instance for whom the model is being deleted.
        db (orm.Session): The database session object.
    """
    model = await model_selector(model_id, user, db)

    db.delete(model)
    db.commit()
