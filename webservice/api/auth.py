"""
This module defines the authentication routes for the FastAPI application, specifically
handling the generation of access tokens for users.

It includes the following functionalities:

- **Login for Access Token**: A POST endpoint that allows users to authenticate
  and receive an access token. The endpoint requires the user's credentials
  (username and password) and validates them against a fake user database.
  Upon successful authentication, it generates an access token that can be
  used for subsequent requests.

Dependencies:
- FastAPI: A modern web framework for building APIs with Python.
- OAuth2PasswordRequestForm: A form to capture username and password for OAuth2 authentication.
- Token: A data model representing the structure of the token response.

Functions:
- `login_for_access_token`: Authenticates a user and returns a token if successful.
  Raises an HTTP 401 error if the credentials are incorrect.

Constants:
- `ACCESS_TOKEN_EXPIRE_MINUTES`: The duration in minutes for which the access token is valid.
- `fake_users_db`: A mock database containing user credentials for authentication.

Usage:
Import this module into the FastAPI application and include the router to enable
authentication routes.
"""

from datetime import timedelta
from typing import Annotated

from fastapi import Depends, APIRouter, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from fRAGme.models.v1.auth import Token
from fRAGme.util.v1.auth import (
    authenticate_user,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    create_access_token,
    fake_users_db,
)

router = APIRouter()


@router.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    """
    Authenticates a user and issues an access token.

    This endpoint allows users to log in by providing their username and password.
    It validates the credentials against a fake user database. If the credentials
    are correct, an access token is generated and returned. If the credentials
    are incorrect, an HTTP 401 Unauthorized error is raised.

    Args:
        form_data (OAuth2PasswordRequestForm): The form containing the user's
        username and password, automatically parsed by FastAPI.

    Returns:
        Token: A data model containing the access token and its type.

    Raises:
        HTTPException: If the username or password is incorrect, an HTTP 401
        Unauthorized error is raised with a relevant message.
    """
    user = authenticate_user(fake_users_db(), form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")
