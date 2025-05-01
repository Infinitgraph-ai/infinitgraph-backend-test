"""
Authentication module for Infinitgraph.ai Backend Developer Technical Test.

This file contains authentication functions that need to be implemented by the candidate.
Key tasks:
1. Implement user authentication against fixed user credentials (for test simplicity)
2. Implement JWT token creation and validation
3. Create a dependency for protecting endpoints

"""

import bcrypt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from typing import Optional
from app.models import UserOut, UserRole
import datetime
from jose import jwt , JWTError 
from dotenv import load_dotenv
import os

load_dotenv()

# You may use a fixed set of credentials for this test
DUMMY_USERS = {
    "admin": {
        "id": 1,
        "username": "admin",
        "email": "admin@infinitgraph.ai",
        "hashed_password": bcrypt.hashpw("adminpass".encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),  # "adminpass"
        "role": UserRole.ADMIN,
        "is_active": True,
        "created_at": datetime.datetime(2023, 1, 1, 0, 0, 0)
    },
    "user": {
        "id": 2,
        "username": "user",
        "email": "user@example.com",
        "hashed_password": bcrypt.hashpw("userpass".encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),  # "userpass"
        "role": UserRole.USER,
        "is_active": True,
        "created_at": datetime.datetime(2023, 2, 1, 0, 0, 0)
    }
}

# Initialize OAuth2 with Bearer Token scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/token")

def authenticate_user(username: str, password: str) -> Optional[UserOut]:
    """
    Verify username and password combination.
    
    Args:
        username: User's username
        password: User's plain text password
        
    Returns:
        UserOut object if authentication is successful, None otherwise
    """
    # 1. Check if username exists in DUMMY_USERS
    if username not in DUMMY_USERS:
        return None
    # 2. Verify the password hash
    if not verify_password(password, DUMMY_USERS[username]["hashed_password"]):
        return None
    # 3. Convert to UserOut model and return
    user_data = DUMMY_USERS[username]
    return UserOut(**user_data)


def create_access_token(data: dict) -> str:
    """
    Create a JWT access token.
    
    Args:
        data: Payload data to encode in the token
        
    Returns:
        JWT token string
    """
    secret = os.getenv("JWT_SECRET_KEY")
    algorithm = os.getenv("JWT_ALGORITHM", "HS256")

    if not secret:
        raise ValueError("JWT_SECRET_KEY is not set.")

    data_copy = data.copy()
    now = datetime.datetime.now(datetime.UTC)
    data_copy.update({
        "exp": now + datetime.timedelta(minutes=30),
        "iat": now
    })

    return jwt.encode(data_copy, secret, algorithm=algorithm)


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
    # 1. Define the credentials_exception
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    # 2. Try to decode the JWT token
    try:
        payload = jwt.decode(token, os.getenv("JWT_SECRET_KEY"), algorithms=[os.getenv("JWT_ALGORITHM", "HS256")])
    except JWTError:
        raise credentials_exception
    # 3. Extract the username from the token
    username: str = payload.get("sub")

    # 4. Look up the user in DUMMY_USERS
    if username not in DUMMY_USERS:
        raise credentials_exception
    # 5. Convert to UserOut model and return
    user_data = DUMMY_USERS[username]
    return UserOut(**user_data)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain text password against a hashed password.
    
    Args:
        plain_password: User's plain text password
        hashed_password: Hashed password from the database
        
    Returns:
        True if the password is correct, False otherwise
    """
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))
    


