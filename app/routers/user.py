from fastapi import APIRouter, Response, Depends, HTTPException
from uuid import UUID
from starlette import status
from database import LocalSession
from models.user import UserModel, CreateUserModel, UpdateUserModel, UpdatePasswordUserModel
from sqlalchemy.orm import Session
from schemas import User
from datetime import datetime
from database import get_db_context
from services import user_service, auth_service
from services.http_exception import http_notfound, http_forbidden, http_badrequest

router = APIRouter(prefix="/user", tags=["user"])

@router.get("", response_model=list[UserModel], status_code=status.HTTP_200_OK)
async def all_user(
        db: Session = Depends(get_db_context),
        user: User = Depends(auth_service.token_interceptor)):
    if not user.is_admin:
        raise http_forbidden()
    return user_service.get_all_users(User, db)


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_user(
        request: CreateUserModel,
        db: Session = Depends(get_db_context),
        user: User = Depends(auth_service.token_interceptor)):
    if not user.is_admin:
        raise http_forbidden()
    return user_service.create_user(request, db)

@router.get("/{user_id}", response_model=UserModel, status_code=status.HTTP_200_OK)
async def get_user_id(
        user_id: UUID,
        db: Session = Depends(get_db_context),
        user: User = Depends(auth_service.token_interceptor)):
    if not user.is_admin:
        raise http_forbidden()
    return user_service.get_user_by_id(user_id, db)

@router.put("/{user_id}", status_code=status.HTTP_200_OK)
async def update_user(
        user_id: UUID,
        request: UpdateUserModel,
        db: Session = Depends(get_db_context),
        user: User = Depends(auth_service.token_interceptor)):
    if not user.is_admin:
        raise http_forbidden()
    return user_service.update_user(user_id, request, db)


@router.put("/updatepassword/{user_id}", status_code=status.HTTP_200_OK)
async def update_password_user(
        user_id: UUID,
        request: UpdatePasswordUserModel,
        db: Session = Depends(get_db_context),
        user: User = Depends(auth_service.token_interceptor)):
    if not user.is_admin:
        raise http_forbidden()
    return user_service.update_password_user(user_id, request, db)

@router.delete("/{user_id}", status_code=status.HTTP_200_OK)
async def delete_user(
        user_id: UUID,
        db: Session = Depends(get_db_context),
        user: User = Depends(auth_service.token_interceptor)):
    if not user.is_admin:
        raise http_forbidden()
    return user_service.delete_user(user_id, UserModel, db)