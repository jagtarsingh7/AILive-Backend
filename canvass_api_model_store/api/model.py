"""Module containing model routes defined for this API."""

from typing import List

from api.v1.model_store import services
from fastapi import APIRouter, Depends, HTTPException, security
from models import schemas
from sqlalchemy import orm

model_router = APIRouter(prefix="/model")


@model_router.post("/api", status_code=201)
async def create_model(
    model: schemas.ModelCreate,
    user: schemas.User = Depends(services.get_current_user),
    db: orm.Session = Depends(services.get_db),
):
    return await services.create_model(user=user, db=db, model=model)


@model_router.delete("/api/{model_id}", status_code=204)
async def delete_model(
    model_id: int,
    user: schemas.User = Depends(services.get_current_user),
    db: orm.Session = Depends(services.get_db),
):
    await services.delete_model(model_id, user, db)
    return {"message", "Successfully Deleted"}
