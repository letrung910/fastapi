from uuid import UUID, uuid4
from sqlalchemy.orm import Session
from schemas.task import Task
from models.task import TaskModel, UpdateTaskModel
from datetime import datetime
from fastapi import HTTPException, status
from .user_service import get_company_id_by_user_id, get_user_by_company_id
from services.http_exception import http_notfound, http_forbidden, http_badrequest

def get_all_tasks(user_id: UUID, user_is_admin: bool, company_id: UUID, db: Session):
    if not user_is_admin:
        # get_company_id = get_company_id_by_user_id(user_id, db)

        tasks = db.query(Task).filter(Task.user_id == user_id).all()
        if not tasks:
            raise http_notfound("No tasks found")
        return tasks

    else:
        get_user = get_user_by_company_id(company_id, db)
        all_tasks = []
        for id in get_user:
            print(f"id: {id}")
            user_tasks = db.query(Task).filter(Task.user_id == id).all()
            if user_tasks:
                all_tasks.extend(user_tasks)

        if not all_tasks:
            raise http_notfound("No tasks found")
        return all_tasks


def create_task(model: TaskModel, user_id: UUID, db: Session):
    if model.priority == "":
        raise http_badrequest("Priority is required")
    if model.status == "":
        raise http_badrequest("Status is required")

    task = Task(
        id=uuid4(),
        user_id=user_id,
        summary=model.summary,
        description=model.description,
        status=model.status,
        priority=model.priority,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return f"Create {model.summary} successful"


def update_task(model: UpdateTaskModel, task_id: UUID, user_id: UUID, db: Session):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise http_notfound("Task not found")
    if model.priority == "":
        raise http_badrequest("Priority is required")
    if model.status == "":
        raise http_badrequest("Status is required")
    task.summary = model.summary
    task.description = model.description
    task.status = model.status
    task.priority = model.priority
    task.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(task)
    return f"Update {task.id} successful"

def delete_task(task_id: UUID, user_id: UUID, db: Session):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise http_notfound("Task not found")
    db.delete(task)
    db.commit()
    return f"Delete {task.id} successful"

def get_task_by_id(task_id: UUID, user_id: UUID, db: Session):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise http_notfound("Task not found")
    if task.user_id != user_id:
        raise http_forbidden("User is not authorized to view this task")
    return task

def get_task_by_user_id(user_id: UUID, db: Session):
    task = db.query(Task).filter(Task.user_id == user_id).all()
    if not task:
        raise http_notfound("Task not found")
    return task

def get_task_by_company_id(company_id: UUID, db: Session):
    get_user = get_user_by_company_id(company_id, db)
    if not get_user:
        raise http_notfound("User not found")
    all_tasks = []
    for id in get_user:
        print(f"id: {id}")
        user_tasks = db.query(Task).filter(Task.user_id == id).all()
        if user_tasks:
            all_tasks.extend(user_tasks)

    if not all_tasks:
        raise http_notfound("Task not found")
    return all_tasks

