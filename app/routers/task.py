from fastapi import APIRouter, Response, Depends, HTTPException
from uuid import UUID
from starlette import status
from database import LocalSession
from models.task import TaskModel, UpdateTaskModel
from sqlalchemy.orm import Session
from schemas import Task, User
from datetime import datetime
from database import get_db_context
from services import task_service, auth_service
from services.http_exception import http_notfound, http_forbidden, http_badrequest


router = APIRouter(prefix="/task", tags=["task"])

@router.get("", response_model=list[TaskModel], status_code=status.HTTP_200_OK)
async def get_all_tasks(
        db: Session = Depends(get_db_context),
        user: User = Depends(auth_service.token_interceptor)):
    if not user.is_active:
        raise http_forbidden()
    return task_service.get_all_tasks(user.id, user.is_admin, user.company_id, db)

@router.post("", status_code=status.HTTP_201_CREATED)
async def create_task(
        task: TaskModel,
        db: Session = Depends(get_db_context),
        user: User = Depends(auth_service.token_interceptor)):
    if not user.is_active:
        raise http_forbidden()
    if task.priority == "":
        raise http_badrequest("Priority is required")
    if task.status == "":
        raise http_badrequest("Status is required")
    return task_service.create_task(task, user.id, db)


@router.put("/{task_id}", status_code=status.HTTP_200_OK)
async def update_task(
        task_id: UUID,
        task: UpdateTaskModel,
        db: Session = Depends(get_db_context),
        user: User = Depends(auth_service.token_interceptor)):
    if not user.is_active:
        raise http_forbidden(detail="User is not active")
    # Get the task to check ownership (this could be moved to the service)
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if not db_task:
        raise http_notfound(detail="Task not found")
    # Check if user is authorized to update this task
    if not user.is_admin and user.id != str(db_task.user_id):
        print (f"User ID: {user.id}, Task User ID: {db_task.user_id}")
        raise http_forbidden(detail="User is not authorized to update this task")

    return task_service.update_task(task, task_id, user.id, db)

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
        task_id: UUID,
        db: Session = Depends(get_db_context),
        user: User = Depends(auth_service.token_interceptor)):
    if not user.is_active:
        raise http_forbidden(detail="User is not active")
    # Get the task to check ownership (this could be moved to the service)
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if not db_task:
        raise http_notfound(detail="Task not found")
    # Check if user is authorized to delete this task
    if not user.is_admin and user.id != str(db_task.user_id):
        print (f"User ID: {user.id}, Task User ID: {db_task.user_id}")
        raise http_forbidden(detail="User is not authorized to delete this task")

    return task_service.delete_task(task_id, user.id, db)

@router.get("/{task_id}", response_model=TaskModel, status_code=status.HTTP_200_OK)
async def get_task_by_id(
        task_id: UUID,
        db: Session = Depends(get_db_context),
        user: User = Depends(auth_service.token_interceptor)):
    if not user.is_active:
        raise http_forbidden(detail="User is not active")
    # Get the task to check ownership (this could be moved to the service)
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if not db_task:
        raise http_notfound(detail="Task not found")
    # Check if user is authorized to get this task
    if not user.is_admin and user.id != str(db_task.user_id):
        print (f"User ID: {user.id}, Task User ID: {db_task.user_id}")
        raise http_forbidden(detail="User is not authorized to get this task")

    return db_task

@router.get("/user/{user_id}", response_model=list[TaskModel], status_code=status.HTTP_200_OK)
async def get_tasks_by_user_id(
        user_id: UUID,
        db: Session = Depends(get_db_context),
        current_user: User = Depends(auth_service.token_interceptor)):
    if not current_user.is_active:
        raise http_forbidden(detail="User is not active")
    # Check if the current user is an admin
    if not current_user.is_admin and current_user.id != str(user_id):
        raise http_forbidden(detail="User is not authorized to view tasks of other users")

    return task_service.get_task_by_user_id(user_id, db)

@router.get("/company/{company_id}", response_model=list[TaskModel], status_code=status.HTTP_200_OK)
async def get_task_by_company_id(
        company_id: UUID,
        db: Session = Depends(get_db_context),
        current_user: User = Depends(auth_service.token_interceptor)):

    # Check if the current user is an admin
    if not current_user.is_admin and current_user.company_id != str(company_id):
        raise http_forbidden(detail="User is not authorized to view tasks of other company")

    return task_service.get_task_by_company_id(company_id, db)
