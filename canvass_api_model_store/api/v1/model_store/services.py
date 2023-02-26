"""Module containing services for auth routes."""

import os

import jwt
import models.models as _models
import models.schemas as _schemas
from fastapi import Depends, HTTPException, security
from models.database import SessionLocal
from passlib import hash
from sqlalchemy import orm

oauth2schema = security.OAuth2PasswordBearer(tokenUrl="/auth/api/token")

JWT_SECRET = os.environ.get("JWT_SECRET")
TOKEN_TYPE = os.environ.get("TOKEN_TYPE")


def get_db():
    """Function to get the database session object."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_current_user(
    db: orm.Session = Depends(get_db),
    token: str = Depends(oauth2schema),
):
    """Function to get current loggedin user."""
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        user = db.query(_models.User).get(payload["id"])
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid Email or Password")

    return _schemas.User.from_orm(user)


async def create_model(user: _schemas.User, db: orm.Session, model: _schemas.ModelCreate):
    """Function to create new model."""
    model = _models.Model(**model.dict(), user_id=user.id)
    db.add(model)
    db.commit()
    db.refresh(model)

    return _schemas.Model.from_orm(model)


async def model_selector(model_id: int, user: _schemas.User, db: orm.Session):
    model = (
        db.query(_models.Model)
        .filter_by(user_id=user.id)
        .filter(_models.Model.id == model_id)
        .first()
    )

    if model is None:
        raise HTTPException(status_code=404, detail="Model does not exist")

    return model


async def delete_model(model_id: int, user: _schemas.User, db: orm.Session):
    model = await model_selector(model_id, user, db)

    db.delete(model)
    db.commit()
