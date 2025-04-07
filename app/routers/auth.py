
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from database import get_db_context
router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/token")
async def login_for_access_token(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: Session = Depends(get_db_context)):
    # user
    return {
        "access_token": "",
        "token_type": "bearer"
    }
