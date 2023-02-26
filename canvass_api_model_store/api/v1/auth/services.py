"""Module containing services for auth routes.

Attributes:
    oauth2schema: An instance of `security.OAuth2PasswordBearer` for retrieving OAuth2 tokens.
    JWT_SECRET (str): The secret key used for JWT encoding.
    TOKEN_TYPE (str): The type of token used for authentication.

"""

import os
from api import constants
import jwt
import models.models as _models
import models.schemas as _schemas
from fastapi import Depends, HTTPException, security
from models.database import SessionLocal
from passlib import hash
from sqlalchemy import orm
from sqlalchemy.exc import SQLAlchemyError

oauth2schema = security.OAuth2PasswordBearer(tokenUrl="/auth/api/token")

JWT_SECRET = os.environ.get("JWT_SECRET")
TOKEN_TYPE = os.environ.get("TOKEN_TYPE")


def get_db():
    """Function to get the database session object.

    Returns:
        sqlalchemy.orm.Session: A SQLAlchemy database session object.

    Raises:
        HTTPException: If there is an error accessing the database.
    """
    db = SessionLocal()
    try:
        yield db
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=constants.Internal_Server_Error, detail="Database Error")
    finally:
        db.close()


async def get_user_by_email(email: str, db: orm.Session):
    """Function get user by email.
    Args:
        email (str): The email address of the user to retrieve.
        db (sqlalchemy.orm.Session): The database session object.

    Returns:
        models.models.User: The user object matching the specified email address.
    """
    return db.query(_models.User).filter(_models.User.email == email).first()


async def create_user(user: _schemas.UserCreate, db: orm.Session):
    """Function to create new user.

    Args:
        user (models.schemas.UserCreate): The user object to create.
        db (sqlalchemy.orm.Session): The database session object.

    Returns:
        models.models.User: The newly created user object.
    """
    user_obj = _models.User(
        email=user.email,
        name=user.name,
        org=user.org,
        hashed_password=hash.bcrypt.hash(user.hashed_password),
    )
    db.add(user_obj)
    db.commit()
    db.refresh(user_obj)
    return user_obj


async def authenticate_user(email: str, password: str, db: orm.Session):
    """Function to authenticate user.

    Args:
        email (str): The email address of the user to authenticate.
        password (str): The password of the user to authenticate.
        db (sqlalchemy.orm.Session): The database session object.

    Returns:
        models.models.User: The authenticated user object.
    """
    user = await get_user_by_email(db=db, email=email)

    if not user:
        return False

    if not user.verify_password(password):
        return False

    return user


async def create_token(user: _models.User):
    """Function to create token.

    Args:
        user (models.models.User): The user object to create a token for.

    Returns:
        dict: A dictionary containing the authentication token and token type.
    """
    user_obj = _schemas.User.from_orm(user)

    token = jwt.encode(user_obj.dict(), JWT_SECRET)

    return dict(access_token=token, token_type=TOKEN_TYPE)


async def get_current_user(
    db: orm.Session = Depends(get_db),
    token: str = Depends(oauth2schema),
):
    """Function to get current loggedin user.

    Args:
        db (orm.Session): The SQLAlchemy session object.
        token (str): The JSON Web Token (JWT) for authentication.

    Returns:
        _schemas.User: The current logged-in user.

    Raises:
        HTTPException: If the token is invalid or the user cannot be retrieved from the database.
    """
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        user = db.query(_models.User).get(payload["id"])
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=constants.Unauthorized, detail="Invalid Email or Password")

    return _schemas.User.from_orm(user)
