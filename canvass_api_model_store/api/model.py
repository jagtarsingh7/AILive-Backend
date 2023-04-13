"""Module containing model routes defined for this API.

Attributes:
    model_router (fastapi.APIRouter): The router for the model routes.
"""

from typing import Dict, List
import models.models as _models
from api.v1.auth import services as auth_serv
from api.v1.model_store import services as model_serv
from fastapi import APIRouter, Body, Depends, Form, HTTPException, status, UploadFile, File
from models import schemas
from sqlalchemy import orm

import os
from azure.storage.blob import BlobServiceClient

model_router = APIRouter(prefix="/api/models")

AZURE_STORAGE_CONNECTION_STRING = os.environ.get("AZURE_STORAGE_CONNECTION_STRING")
AZURE_STORAGE_CONTAINER_NAME = "models"


@model_router.post("/upload-file/")
async def upload_file(file: UploadFile = File(...)):
    return await model_serv.upload_file(file=file)


@model_router.post("", status_code=status.HTTP_201_CREATED)
async def create_model(
    # model: schemas.ModelCreate=Form(...),
    text:schemas.ModelCreate=Depends(),
    file: UploadFile =File(...),
    user: schemas.User = Depends(auth_serv.get_current_user),
    db: orm.Session = Depends(auth_serv.get_db)
   
):
    """Create a new model.

    Args:
        model (schemas.ModelCreate): The model data.
        user (schemas.User): The current user.
        db (orm.Session): The database session.

    Returns:
        schemas.Model: The id of the created model.

    Raises:
        HTTPException: If there is a database error or the request is unauthorized.
    """
   
    # Add more validation checks as needed
    # return await model_serv.create_model(user=user, db=db, model=model, file=file)
    # text = _models.Model(**text.dict(), user_id=user.id)

    return {"message": f"Successfully Deleted Model with id:{text}"}

@model_router.delete("/{model_id}", status_code=status.HTTP_200_OK)
async def delete_model(
    model_id: int,
    user: schemas.User = Depends(auth_serv.get_current_user),
    db: orm.Session = Depends(auth_serv.get_db),
):
    """Delete an existing model.

    Args:
        model_id (int): The ID of the model to delete.
        user (schemas.User): The current user.
        db (orm.Session): The database session.

    Returns:
        dict: A message indicating success.

    Raises:
        HTTPException: If the model does not exist, there is a database error, or the request is unauthorized.
    """
    await model_serv.delete_model(model_id, user, db)
    return {"message": f"Successfully Deleted Model with id: {model_id}"}


@model_router.patch("/{model_id}")
async def update_model(
    model_id: int,
    model: schemas.ModelUpdate,
    user: schemas.User = Depends(auth_serv.get_current_user),
    db: orm.Session = Depends(auth_serv.get_db),
) -> schemas.Model:
    """Update an existing model.

    Args:
        model_id (int): The ID of the model to be updated.
        model (schemas.ModelUpdate): The updated model data.
        user (schemas.User): The current user.
        db (orm.Session): The database session.

    Returns:
        schemas.Model: The updated model.

    Raises:
        HTTPException: If the model does not exist, there is a database error, or the request is unauthorized.
    """
    return await model_serv.update_model(user=user, db=db, model=model, model_id=model_id)


"""added get models to get models"""


@model_router.get("/{model_id}", status_code=status.HTTP_200_OK)
async def read_model(
    model_id: int,
    user: schemas.User = Depends(auth_serv.get_current_user),
    db: orm.Session = Depends(auth_serv.get_db),
):
    model_display = await model_serv.read_model(user.id, model_id, db)
    return {"model": model_display}


@model_router.get("/", status_code=status.HTTP_200_OK)
async def read_all_models(
    user: schemas.User = Depends(auth_serv.get_current_user),
    db: orm.Session = Depends(auth_serv.get_db),
):
    model_display = await model_serv.read_all_models(user.id, db)
    return {"model": model_display}
