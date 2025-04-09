from typing import Optional
from sqlalchemy.orm import Session
from schemas import User
from .hash_service import verify_password
from datetime import datetime, timedelta
from jose import JWTError, jwt
from settings import JWT_SECRET, JWT_ALGORITHM
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status

oa2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")

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
        "exp": datetime.utcnow()
    }
    return jwt.encode(claims, JWT_SECRET, algorithm=JWT_ALGORITHM)



def token_interceptor(token: str = Depends(oa2_bearer), algorithm: str = JWT_ALGORITHM):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[algorithm])
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
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )