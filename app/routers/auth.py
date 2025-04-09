from fastapi import APIRouter, Depends, HTTPException, Body, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from database import get_db_context
from services import auth_service
from datetime import timedelta
from typing import Dict

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/token")
async def login_for_access_token(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: Session = Depends(get_db_context)):
    """
    Login endpoint that returns both access and refresh tokens
    """
    user = auth_service.authenticate_user(
        form_data.username, form_data.password, db
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create both access and refresh tokens
    tokens = auth_service.create_tokens(user)

    return tokens


@router.post("/refresh")
async def refresh_token(
        refresh_token: str = Body(..., embed=True)):
    """
    Use a valid refresh token to get a new access token
    """
    try:
        new_token = auth_service.refresh_access_token(refresh_token)
        return new_token
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error refreshing token: {str(e)}"
        )


@router.post("/logout", status_code=status.HTTP_200_OK)
async def logout(
        refresh_token: str = Body(..., embed=True)):
    """
    Logout by revoking the refresh token
    """
    try:
        return auth_service.revoke_refresh_token(refresh_token)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error logging out: {str(e)}"
        )
