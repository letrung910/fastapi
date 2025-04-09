from typing import Optional, Dict, Tuple
from sqlalchemy.orm import Session
from schemas import User
from .hash_service import verify_password
from datetime import datetime, timedelta
from jose import JWTError, jwt
from settings import JWT_SECRET, JWT_ALGORITHM, REFRESH_TOKEN_EXPIRE_DAYS
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
import uuid
from settings import redis_client

oa2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")
  # Default to 30 days if not set

def authenticate_user(username: str, password: str, db: Session):
    user = db.query(User).filter(User.username == username).first()

    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(user: User, expires: Optional[timedelta] = None):
    claims = {
        "sub": user.username,
        "id" : str(user.id),
        "first_name": user.first_name,
        "last_name": user.last_name,
        "is_admin": user.is_admin,
        "exp": datetime.utcnow() + (expires if expires else timedelta(minutes=15)),
    }
    return jwt.encode(claims, JWT_SECRET, algorithm=JWT_ALGORITHM)


def create_refresh_token(user: User, expires: Optional[timedelta] = None):
    token_jti = str(uuid.uuid4())  # Generate unique token ID
    expires_delta = expires if expires else timedelta(
        days=REFRESH_TOKEN_EXPIRE_DAYS)
    exp = datetime.utcnow() + expires_delta

    claims = {
        "sub": user.username,
        "id": str(user.id),
        "token_type": "refresh",
        "jti": token_jti,  # Include unique token ID
        "exp": exp,
    }

    token = jwt.encode(claims, JWT_SECRET, algorithm=JWT_ALGORITHM)

    # Save refresh token in Redis
    expiry_seconds = int(expires_delta.total_seconds())
    redis_client.setex(
        f"refresh_token:{user.id}:{token_jti}",
        expiry_seconds,
        "valid"
    )

    return token


def create_tokens(user: User) -> Dict[str, str]:
    """Create both access and refresh tokens"""
    access_token = create_access_token(user)
    refresh_token = create_refresh_token(user)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


def refresh_access_token(refresh_token: str) -> Dict[str, str]:
    """Create new access token using refresh token"""
    try:
        payload = jwt.decode(refresh_token, JWT_SECRET,
                             algorithms=[JWT_ALGORITHM])

        # Verify this is a refresh token
        if payload.get("token_type") != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token",
                headers={"WWW-Authenticate": "Bearer"},
            )

        user_id = payload.get("id")
        token_jti = payload.get("jti")

        # Check if token exists in Redis and is valid
        token_key = f"refresh_token:{user_id}:{token_jti}"
        token_status = redis_client.get(token_key)

        if not token_status:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Refresh token not found",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # If decode_responses=True is set in redis_client
        if token_status != "valid":
            # Or for byte comparison: if token_status != b"valid":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Refresh token has been revoked",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Create a temporary user object to generate new tokens
        user = User()
        user.id = user_id
        user.username = payload.get("sub")

        # Get user details from database if needed
        # db_user = db.query(User).filter(User.id == user_id).first()

        # Generate new access token
        access_token = create_access_token(user)

        return {
            "access_token": access_token,
            "token_type": "bearer"
        }

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )


def revoke_refresh_token(refresh_token: str):
    """Invalidate a refresh token"""
    try:
        payload = jwt.decode(refresh_token, JWT_SECRET,
                             algorithms=[JWT_ALGORITHM])
        user_id = payload.get("id")
        token_jti = payload.get("jti")

        # Delete token from Redis
        redis_client.delete(f"refresh_token:{user_id}:{token_jti}")

        return {"message": "Token successfully revoked"}
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )


def token_interceptor(token: str = Depends(oa2_bearer)):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        user = User()
        user.username: str = payload.get("sub")
        user.id: str = payload.get("id")
        user.first_name: str = payload.get("first_name")
        user.last_name: str = payload.get("last_name")
        user.is_admin: str = payload.get("is_admin")
        if user.username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return user
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )