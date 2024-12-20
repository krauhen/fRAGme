from pydantic import BaseModel


class Token(BaseModel):
    """
    Represents an access token.

    Attributes:
        access_token (str): The JWT access token.
        token_type (str): The type of token (e.g., "bearer").
    """

    access_token: str
    token_type: str


class TokenData(BaseModel):
    """
    Represents the data contained within a token.

    Attributes:
        username (str | None): The username associated with the token, or None if not provided.
    """

    username: str | None = None


class User(BaseModel):
    """
    Represents a user in the system.

    Attributes:
        username (str): The unique username of the user.
        email (str | None): The email address of the user, or None if not provided.
        full_name (str | None): The full name of the user, or None if not provided.
        disabled (bool | None): Indicates whether the user is disabled, or None if not specified.
    """

    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None


class UserInDB(User):
    """
    Represents a user stored in the database.

    Inherits from the User class and adds an attribute for the hashed password.

    Attributes:
        hashed_password (str): The hashed password of the user.
    """

    hashed_password: str
