"""Module containing services for auth routes.

This module provides functions for creating a new model, selecting, updating,
retrieving and deleting a model.

Functions:
    create_model: Function to create a new model.
    model_selector: Function to select a model.
    delete_model: Function to delete a model.

Attributes:
    logger: Instance of logging to show FastAPI messages
"""

import logging
from operator import and_
from typing import Dict

import models.models as _models
import models.schemas as _schemas
from fastapi import HTTPException, status, UploadFile, File
from sqlalchemy import orm
from sqlalchemy.exc import NoResultFound, SQLAlchemyError

logger = logging.getLogger(__name__)

import pickle
import os
from azure.storage.blob import BlobServiceClient

AZURE_STORAGE_CONNECTION_STRING = os.environ.get("AZURE_STORAGE_CONNECTION_STRING")
AZURE_STORAGE_CONTAINER_NAME = "models"


async def create_model(
    user: _schemas.User,
    db: orm.Session,
    model: _schemas.ModelCreate,
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
        # Create model in database
        db_model = _models.Model(**model.dict(), user_id=user.id)
        db.add(db_model)
        db.commit()
        db.refresh(db_model)
        model_id = db_model.id

        # # Upload model file to Azure Blob Storage
        # blob_service_client = BlobServiceClient.from_connection_string(
        #     AZURE_STORAGE_CONNECTION_STRING
        # )
        # container_client = blob_service_client.get_container_client(AZURE_STORAGE_CONTAINER_NAME)
        # blob_client = container_client.get_blob_client(f"{model_id}.pkl")
        # pickle_data = pickle.dumps(await model_file.read())
        # blob_client.upload_blob(pickle_data, overwrite=True)

        # Upload model file to Azure Blob Storage
        # blob_service_client = BlobServiceClient.from_connection_string(
        #     AZURE_STORAGE_CONNECTION_STRING
        # )
        # model_file = model_file.dict()
        # container_client = blob_service_client.get_container_client(AZURE_STORAGE_CONTAINER_NAME)
        # blob_client = container_client.get_blob_client(model_file.filename)
        # data = await model_file.read()
        # blob_client.upload_blob(data, overwrite=True)

        # Log success and return model ID
        logger.info(f"Model created with id: {model_id}")
        return {"model_id": model_id}

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


async def upload_file(file: _schemas.ModelUpload):
    try:
        blob_service_client = BlobServiceClient.from_connection_string(
            AZURE_STORAGE_CONNECTION_STRING
        )
        container_client = blob_service_client.get_container_client(AZURE_STORAGE_CONTAINER_NAME)
        blob_client = container_client.get_blob_client(file.filename)
        data = await file.read()
        blob_client.upload_blob(data, overwrite=True)
        return {"message": "File uploaded successfully."}
    except Exception as e:
        return {"message": f"Error uploading file: {e}"}


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
            .filter(_models.Model.user_id == user.id, _models.Model.id == model_id)
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
) -> _schemas.Model:
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

        # Return updated model
        return db_model
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


"""Added get models functions"""


async def read_model(user_id: int, id: int, db: orm.Session):
    return (
        db.query(_models.Model)
        .filter(and_(_models.Model.id == id, _models.Model.user_id == user_id))
        .first()
    )


async def read_all_models(user_id: int, db: orm.Session):
    return db.query(_models.Model).filter(_models.Model.user_id == user_id).all()
