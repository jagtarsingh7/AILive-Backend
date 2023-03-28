"""Module containing model routes defined for this API.

Attributes:
    model_router (fastapi.APIRouter): The router for the model routes.  
"""

from typing import List

from api.v1.auth import services as authServ
from api.v1.model_store import services as modelServ
from fastapi import APIRouter, Depends, status
from models import schemas
from sqlalchemy import orm

model_router = APIRouter(prefix="/model")


@model_router.post("/api", status_code=status.HTTP_201_CREATED)
async def create_model(
    model: schemas.ModelCreate,
    user: schemas.User = Depends(authServ.get_current_user),
    db: orm.Session = Depends(authServ.get_db),
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
    return await modelServ.create_model(user=user, db=db, model=model)


@model_router.delete("/api/{model_id}", status_code=status.HTTP_200_OK)
async def delete_model(
    model_id: int,
    user: schemas.User = Depends(authServ.get_current_user),
    db: orm.Session = Depends(authServ.get_db),
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
    await modelServ.delete_model(model_id, user, db)
    return {"message": f"Successfully Deleted Model with id: {model_id}"}

"""added get models to get models"""


@model_router.get("/get", status_code=status.HTTP_200_OK)
async def getModel(id:int,user: schemas.User = Depends(authServ.get_current_user),
                   db: orm.Session = Depends(authServ.get_db)):
    modelDisplay= await modelServ.get_model(user.id,id, db) 
    return {"model": modelDisplay}

@model_router.get("/get/all", status_code=status.HTTP_200_OK)
async def getModel_all(user: schemas.User = Depends(authServ.get_current_user),db: orm.Session = Depends(authServ.get_db)):
    
    modelDisplay= await modelServ.get_model_all(user.id,db)
    return {"model": modelDisplay}

# @get_model_router.get("/", status_code=status.HTTP_200_OK)
# async def getme():
#       return {"model": "id"}

