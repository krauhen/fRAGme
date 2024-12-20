import bcrypt
import json
import os
import jwt

from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone
from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from fRAGme.models.v1.auth import User, TokenData, UserInDB

load_dotenv(verbose=True, override=True)

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def fake_users_db():
    """Load and return the fake user database from a JSON file.

    Returns:
        dict: A dictionary containing user data loaded from the fake_db.json file.
    """
    db = dict()
    db["admin"] = dict()
    db["admin"]["username"] = "admin"
    db["admin"]["hashed_password"] = os.getenv("ADMIN_SECRET")

    return db


def verify_password(plain_password, hashed_password):
    """Verify if the provided plain password matches the hashed password.

    Args:
        plain_password (str): The plain password to verify.
        hashed_password (str): The hashed password to compare against.

    Returns:
        bool: True if the passwords match, False otherwise.
    """
    password_byte_enc = plain_password.encode("utf-8")
    hashed_password_byte_enc = hashed_password.encode("utf-8")
    return bcrypt.checkpw(
        password=password_byte_enc, hashed_password=hashed_password_byte_enc
    )


def get_password_hash(password):
    """Generate a hashed password from the provided plain password.

    Args:
        password (str): The plain password to be hashed.

    Returns:
        bytes: The hashed password in bytes.
    """
    pwd_bytes = password.encode("utf-8")
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password=pwd_bytes, salt=salt)
    return hashed_password


def get_user(db, username: str):
    """Retrieve a user from the database by username.

    Args:
        db (dict): The database containing user information.
        username (str): The username of the user to retrieve.

    Returns:
        UserInDB: An instance of UserInDB containing user data if found; None otherwise.
    """
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def authenticate_user(fake_db, username: str, password: str):
    """Authenticate a user by verifying their username and password.

    Args:
        fake_db (dict): The fake database containing user information.
        username (str): The username of the user to authenticate.
        password (str): The password provided by the user.

    Returns:
        UserInDB: An instance of UserInDB if authentication is successful; False otherwise.
    """
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    """Create an access token with an optional expiration time.

    Args:
        data (dict): The data to encode in the token.
        expires_delta (timedelta, optional): The duration for which the token is valid.

    Returns:
        str: The encoded JWT access token.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    """Retrieve the current user based on the provided token.

    Args:
        token (str): The JWT access token.

    Raises:
        HTTPException: If the credentials are invalid or user not found.

    Returns:
        User: The authenticated User instance.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except Exception as e:
        raise credentials_exception
    user = get_user(fake_users_db(), username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
):
    """Ensure the current user is active.

    Args:
        current_user (User): The current authenticated user.

    Raises:
        HTTPException: If the user is inactive.

    Returns:
        User: The active User instance.
    """
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


if __name__ == "__main__":
    plain_password = "test"
    print(plain_password)
    hashed_password = get_password_hash(plain_password)
    print(hashed_password)
