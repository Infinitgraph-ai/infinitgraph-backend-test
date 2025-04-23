"""
Authentication module for Infinitgraph.ai Backend Developer Technical Test.

This file contains authentication functions that need to be implemented by the candidate.
Key tasks:
1. Implement user authentication against fixed user credentials (for test simplicity)
2. Implement JWT token creation and validation
3. Create a dependency for protecting endpoints

"""

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from typing import Optional
from models import UserOut, UserRole
import datetime

# You may use a fixed set of credentials for this test
DUMMY_USERS = {
    "admin": {
        "id": 1,
        "username": "admin",
        "email": "admin@infinitgraph.ai",
        "hashed_password": "$2b$12$UwWN8ZFAg6F.OHqlchQgKepKVPhKFAyESOQqJIcQjTB8yDQJA05ca",  # "adminpass"
        "role": UserRole.ADMIN,
        "is_active": True,
        "created_at": datetime.datetime(2023, 1, 1, 0, 0, 0)
    },
    "user": {
        "id": 2,
        "username": "user",
        "email": "user@example.com",
        "hashed_password": "$2b$12$3lrVx9U4sFkLp9yX42yCXO0S0AeDtvdDX66zYDGAK5Gwe0gj3pGcq",  # "userpass"
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
    pass


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
    pass


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
    # TODO: Implement current user extraction from token
    # 1. Define the credentials_exception
    # 2. Try to decode the JWT token
    # 3. Extract the username from the token
    # 4. Look up the user in DUMMY_USERS
    # 5. Convert to UserOut model and return
    pass