"""Module containing auth routes defined for this API."""

from typing import List

from api.v1.auth import services
from fastapi import APIRouter, Depends, HTTPException, security, status
from models import schemas
from sqlalchemy import orm

auth_router = APIRouter(prefix="/auth")


@auth_router.post("/api/users")
async def create_user(new_user: schemas.UserCreate, db: orm.Session = Depends(services.get_db)):
    """
    Route to create users.

    Args:
        user (schemas.UserCreate): User object to be created.
        db (orm.Session): SQLAlchemy session to connect to the database.

    Raises:
        HTTPException: If email is already in use.
        HTTPException: If an internal server error occurs.

    Returns:
        A token for the created user.
    """

    db_user = await services.get_user_by_email(new_user.email, db)
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already in use")

    try:
        new_user = await services.create_user(new_user, db)

        return await services.create_token(new_user)

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error"
        )


@auth_router.post("/api/token")
async def generate_token(
    form_data: security.OAuth2PasswordRequestForm = Depends(),
    db: orm.Session = Depends(services.get_db),
):
    """
    Route to create tokens.

    Args:
        form_data (security.OAuth2PasswordRequestForm): Form data containing username and password.
        db (orm.Session): SQLAlchemy session to connect to the database.

    Raises:
        HTTPException: If credentials are invalid.

    Returns:
        A token for the authenticated user.
    """
    user = await services.authenticate_user(form_data.username, form_data.password, db)

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Credentials")

    return await services.create_token(user)


@auth_router.get("/api/users/me", response_model=schemas.User)
async def get_user(user: schemas.User = Depends(services.get_current_user)):
    """
    Route to get the loggedin user.

    Args:
        user (schemas.User): Current user.

    Returns:
        Current user object.
    """
    return user


@auth_router.get("/api")
async def root():
    """Route to get the default route.

    Returns:
        A message indicating the API name and version.
    """
    return {"message": "Canvass AI Live: Model Management API"}
