"""Module containing services for auth routes."""

import os

import jwt
import models.models as _models
import models.schemas as _schemas
from fastapi import Depends, FastAPI, HTTPException, security
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


async def get_user_by_email(email: str, db: orm.Session):
    """Function get user by email."""
    return db.query(_models.User).filter(_models.User.email == email).first()


async def create_user(user: _schemas.UserCreate, db: orm.Session):
    """Function to create new user."""
    user_obj = _models.User(
        email=user.email, name=user.name, hashed_password=hash.bcrypt.hash(user.hashed_password)
    )
    db.add(user_obj)
    db.commit()
    db.refresh(user_obj)
    return user_obj


async def authenticate_user(email: str, password: str, db: orm.Session):
    """Function to authenticate user."""
    user = await get_user_by_email(db=db, email=email)

    if not user:
        return False

    if not user.verify_password(password):
        return False

    return user


async def create_token(user: _models.User):
    """Function to create token."""
    user_obj = _schemas.User.from_orm(user)

    token = jwt.encode(user_obj.dict(), JWT_SECRET)

    return dict(access_token=token, token_type=TOKEN_TYPE)


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
