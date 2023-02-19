"""Module containing model routes defined for this API."""

from typing import List

from api.v1.model_store import services
from fastapi import APIRouter, Depends, HTTPException, security
from models import schemas
from sqlalchemy import orm

model_router = APIRouter(prefix="/model")


@model_router.post("/api")
async def create_model(
    model: schemas.ModelCreate,
    user: schemas.User = Depends(services.get_current_user),
    db: orm.Session = Depends(services.get_db),
):
    return await services.create_model(user=user, db=db, model=model)
