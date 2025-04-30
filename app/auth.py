"""
Authentication module for Infinitgraph.ai Backend Developer Technical Test.

This file contains authentication functions that need to be implemented by the candidate.
Key tasks:
1. Implement user authentication against fixed user credentials (for test simplicity)
2. Implement JWT token creation and validation
3. Create a dependency for protecting endpoints

"""
import datetime
import jwt
import bcrypt

from fastapi import Depends, status
from fastapi.security import OAuth2PasswordBearer

from typing import Optional

from app.models import UserOut, UserRole
from app.core.exceptions import BackendError

# You may use a fixed set of credentials for this test
DUMMY_USERS = {
    "admin": {
        "id": 1,
        "username": "admin",
        "email": "admin@infinitgraph.ai",
        "hashed_password": "$2b$12$MR9qkz9YkqD2Me6jynPc5O9OtFC3uDrKuYgk8WgzBJHaE8osgnlAq",  # "adminpass"
        "role": UserRole.ADMIN,
        "is_active": True,
        "created_at": datetime.datetime(2023, 1, 1, 0, 0, 0)
    },
    "user": {
        "id": 2,
        "username": "user",
        "email": "user@example.com",
        "hashed_password": "$2b$12$StzpD21bEbyFAcOSVThO9.OtwkqpxGIGZqSM88qp5EJJJP4OeZ1Fu",  # "userpass"
        "role": UserRole.USER,
        "is_active": True,
        "created_at": datetime.datetime(2023, 2, 1, 0, 0, 0)
    }
}

# Initialize OAuth2 with Bearer Token scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/token")

# TODO: Implement the authenticate_user function
def authenticate_user(username: str, password: str) -> Optional[UserOut]:
    """
    Verify username and password combination.
    
    Args:
        username: User's username
        password: User's plain text password
        
    Returns:
        UserOut object if authentication is successful, None otherwise
    """
    # TODO: Implement user authentication
    # 1. Check if username exists in DUMMY_USERS
    # 2. Verify the password hash
    # 3. Convert to UserOut model and return
    user = DUMMY_USERS.get(username)
    
    if not user:
        return None

    if not bcrypt.checkpw(password.encode('utf-8'), user.get('hashed_password').encode('utf-8')):
        return None

    return UserOut(
        id=user.get('id'),
        username=user.get('username'),
        email=user.get('email'),
        role=user.get('role'),
        is_active=user.get('is_active'),
        created_at=user.get('created_at'),
    )



# TODO: Implement the create_access_token function
def create_access_token(data: dict) -> str:
    """
    Create a JWT access token.
    
    Args:
        data: Payload data to encode in the token
        
    Returns:
        JWT token string
    """
    # TODO: Implement JWT token creation
    # 1. Create a copy of data
    # 2. Set expiration time (e.g., 30 minutes)
    # 3. Create and return the JWT token

    now = datetime.datetime.now()
    expire = now + datetime.timedelta(minutes=30)
    payload = data.copy()

    payload |= {"exp": expire, "iat": now, "nbf": now, "iss": "infinitgraph.ai"}

    return jwt.encode(payload, key="my-secret-key", algorithm="HS256")


# TODO: Implement the get_current_user dependency
async def get_current_user(token: str = Depends(oauth2_scheme)) -> UserOut:
    """
    Decode and validate the access token to get the current user.
    
    Args:
        token: JWT token from Authorization header
        
    Returns:
        UserOut object for the authenticated user
        
    Raises:
        HTTPException: If token is invalid or user not found
    """
    credentials_exception = BackendError(
        status=status.HTTP_401_UNAUTHORIZED,
        message="Could not validate credentials",
        data={"error": "Invalid token"},
    )

    try:
        payload = jwt.decode(token, key="my-secret-key", algorithms=["HS256"])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except jwt.PyJWTError:
        raise credentials_exception

    user = DUMMY_USERS.get(username)
    if user is None:
        raise credentials_exception

    return UserOut(
        id=user.get('id'),
        username=user.get('username'),
        email=user.get('email'),
        role=user.get('role'),
        is_active=user.get('is_active'),
        created_at=user.get('created_at'),
    )