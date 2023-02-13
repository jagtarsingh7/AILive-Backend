"""Module containing auth routes defined for this API."""

from typing import List

from api.v1.auth import schemas, services
from fastapi import APIRouter, Depends, FastAPI, HTTPException, security
from sqlalchemy import orm

auth_router = APIRouter(prefix="/auth")


@auth_router.post("/api/users")
async def create_user(user: schemas.UserCreate, db: orm.Session = Depends(services.get_db)):
    """Route to create users."""
    db_user = await services.get_user_by_email(user.email, db)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already in use")

    user = await services.create_user(user, db)

    return await services.create_token(user)


@auth_router.post("/api/token")
async def generate_token(
    form_data: security.OAuth2PasswordRequestForm = Depends(),
    db: orm.Session = Depends(services.get_db),
):
    """Route to create tokens."""
    user = await services.authenticate_user(form_data.username, form_data.password, db)

    if not user:
        raise HTTPException(status_code=401, detail="Invalid Credentials")

    return await services.create_token(user)


@auth_router.get("/api/users/me", response_model=schemas.User)
async def get_user(user: schemas.User = Depends(services.get_current_user)):
    """Route to get the loggedin user."""
    return user


@auth_router.get("/api")
async def root():
    """Route to get the default route."""
    return {"message": "Canvass AI Live: Model Management API"}
