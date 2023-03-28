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
import os
from typing import Dict

import models.models as _models
import models.schemas as _schemas
from fastapi import HTTPException, security, status
from sqlalchemy import orm
from sqlalchemy.exc import NoResultFound, SQLAlchemyError

logger = logging.getLogger(__name__)

oauth2schema = security.OAuth2PasswordBearer(tokenUrl="/auth/api/token")

JWT_SECRET = os.environ.get("JWT_SECRET")
TOKEN_TYPE = os.environ.get("TOKEN_TYPE")


async def create_model(
    user: _schemas.User, db: orm.Session, model: _schemas.ModelCreate
) -> Dict[str, int]:
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
    """Function to select a model.

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
            .one_or_none()
        )

        if not model:
            raise NoResultFound
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


async def update_model(
    user: _schemas.User, db: orm.Session, model: _schemas.ModelUpdate, model_id: int
) -> Dict[str, int]:
    """Function to update a model.

    Args:
        user (_schemas.User): The user object.
        db (orm.Session): The database session object.
        model (_schemas.ModelUpdate): The update model object.
        model_id (int): The model id.

    Returns:
        Dict[str, int]: A dictionary containing the model id and updated model version.

    Raises:
        HTTPException: If the model does not exist, there is a database error, or the request is unauthorized.
    """
    try:
        # Find if model for user exists
        db_model = await model_selector(model_id, user, db)

        # Update model with new values
        for attr, value in model.dict(exclude_unset=True).items():
            setattr(db_model, attr, value)

        # Auto increment model version
        db_model.model_version += 1

        # Commit the changes to the database
        db.commit()
        db.refresh(db_model)

        # Return model id and updated model version
        return {"id": db_model.id, "model_version": db_model.model_version}
    except HTTPException as e:
        raise e
    except SQLAlchemyError as e:
        logger.exception(f"Database Error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Database Error: {e}"
        )
    except Exception as e:
        logger.exception(f"Internal Server Error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Internal Server Error: {e}"
        )
