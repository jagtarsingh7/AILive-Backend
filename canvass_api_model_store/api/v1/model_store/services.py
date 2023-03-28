"""Module containing services for auth routes.

This module provides functions for creating a new model, selecting, updating,
retrieving and deleting a model.

Functions:
    create_model: Function to create a new model.
    model_selector: Function to select a model.
    delete_model: Function to delete a model.

Attributes:
    logger: Instance of logging to show FastAPI messages
    oauth2schema: OAuth2PasswordBearer object for token authentication.
    JWT_SECRET: Secret key for JSON Web Token authentication.
    TOKEN_TYPE: Token type for JSON Web Token authentication.
"""

import logging
from operator import and_
import os

import models.models as _models
import models.schemas as _schemas
from fastapi import HTTPException, security, status
from sqlalchemy import orm
from sqlalchemy.exc import SQLAlchemyError, NoResultFound

logger = logging.getLogger(__name__)

oauth2schema = security.OAuth2PasswordBearer(tokenUrl="/auth/api/token")

JWT_SECRET = os.environ.get("JWT_SECRET")
TOKEN_TYPE = os.environ.get("TOKEN_TYPE")


async def create_model(user: _schemas.User, db: orm.Session, model: _schemas.ModelCreate) -> int:
    """Function to create new model.

    Args:
        user (_schemas.User): The user object.
        db (orm.Session): SQLAlchemy database session object.
        model (_schemas.ModelCreate): The model to be created.

    Returns:
        _schemas.Model: The created model object.

    Raises:
        HTTPException: If there is an error during the database operation.

    """
    try:
        model = _models.Model(**model.dict(), user_id=user.id)
        db.add(model)
        db.commit()
        db.refresh(model)
        logger.info(f"Model created with id: {model.id}")
        return {"model_id": model.id}
    except SQLAlchemyError:
        logger.exception("Error during model create SQL execution")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Database error occurred during create model",
        )
    except Exception:
        logger.exception("Internal Server Error.")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error."
        )


async def model_selector(model_id: int, user: _schemas.User, db: orm.Session) -> _schemas.Model:
    """
    Function to select a model.

    Args:
        model_id (int): The ID of the model to be selected.
        user (_schemas.User): The user object.
        db (orm.Session): SQLAlchemy database session object.

    Returns:
        The selected model object.

    Raises:
        HTTPException: If the model does not exist or there is an error during the database operation.
    """
    try:
        model = (
            db.query(_models.Model)
            .filter_by(user_id=user.id)
            .filter(_models.Model.id == model_id)
            .one()
        )
    except NoResultFound:
        logger.exception(f"Model with id {model_id} not found")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Model with id {model_id} does not exist"
        )
    except Exception:
        logger.exception("Internal Server Error.")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error"
        )

    return model


async def delete_model(model_id: int, user: _schemas.User, db: orm.Session):
    """Deletes a model from the database for a given user.

    Args:
        model_id (int): The id of the model to be deleted.
        user (_schemas.User): The user instance for whom the model is being deleted.
        db (orm.Session): The database session object.

    Raises:
        HTTPException: If there is an error during the database operation.
    """
    model = await model_selector(model_id, user, db)

    try:
        db.delete(model)
        db.commit()
        logger.info(f"Model deleted with id: {model.id}")
    except SQLAlchemyError:
        logger.exception("Error during model delete SQL execution")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Database error occurred during model delete",
        )
    except Exception:
        logger.exception("Internal Server Error")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error"
        )

"""Added get models functions"""
async def get_model(user_id:int,id:int ,  db: orm.Session):
    return db.query(_models.Model).filter(and_(_models.Model.id == id, _models.Model.user_id == user_id)).first()

async def get_model_all(user_id:int,db: orm.Session):
    return db.query(_models.Model).filter(_models.Model.user_id == user_id).all()

