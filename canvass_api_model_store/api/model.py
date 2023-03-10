"""Module containing model routes defined for this API.

Attributes:
    model_router (fastapi.APIRouter): The router for the model routes.
"""

from typing import Dict, List

from api.v1.auth import services as authServ
from api.v1.model_store import services as modelServ
from fastapi import APIRouter, Depends, status
from models import schemas
from sqlalchemy import orm

model_router = APIRouter(prefix="/model")


@model_router.put("/update-model/{model_id}")
async def update_model(
    model_id: int,
    model: schemas.ModelUpdate,
    user: schemas.User = Depends(authServ.get_current_user),
    db: orm.Session = Depends(authServ.get_db),
) -> Dict[str, int]:
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
    return await modelServ.update_model(user=user, db=db, model=model, model_id=model_id)
