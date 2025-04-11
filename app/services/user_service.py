from uuid import UUID, uuid4
from sqlalchemy.orm import Session
from schemas import User
from models.user import UserModel, CreateUserModel, UpdateUserModel, UpdatePasswordUserModel
from datetime import datetime
from .hash_service import get_password_hash
from fastapi import HTTPException, status

def create_user(model: CreateUserModel, db: Session):
    if model.company_id == "":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Company id is required")
    if model.username == "":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username is required")
    if model.password == "":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Password is required")
    if model.repeat_password == "":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Repeat password is required")
    if db.query(User).filter(User.username == model.username).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Username {model.username} already exists")
    if model.password != model.repeat_password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Password and repeat password not match")

    user = User(**model.dict(exclude={"password", "repeat_password"}))
    user.id = uuid4()
    user.hashed_password = get_password_hash(model.password)
    user.created_at = datetime.utcnow()
    user.updated_at = datetime.utcnow()
    db.add(user)
    db.commit()
    db.refresh(user)
    return f"Create {model.username} sucessfull"


def update_user(id: UUID, model: UpdateUserModel, db: Session):
    user = get_user_by_id(id, db)
    # return user
    if not user:
        return f"User with id {id} not found"
    user.first_name = model.first_name
    user.last_name = model.last_name
    user.is_active = model.is_active
    user.is_admin = model.is_admin
    user.updated_at = datetime.utcnow()
    db.add(user)
    db.commit()
    print (f"Update {user.username} sucessfull")


def update_password_user(id: UUID, model: UpdatePasswordUserModel, db: Session):
    user = get_user_by_id(id, db)
    if model.password != model.repeat_password:
        return f"Password and repeat password not match"
    # return user
    if not user:
        return f"User with id {id} not found"
    user.hashed_password = get_password_hash(model.password)
    user.updated_at = datetime.utcnow()
    db.add(user)
    db.commit()
    return f"Update password {user.username} sucessfull"

def delete_user(id: UUID, model: UserModel, db: Session):
    user = db.query(User).filter(User.id == id).first()
    if not user:
        return f"User with id {id} not found"
    db.delete(user)
    db.commit()
    return f"Delete {user.username} sucessfull"


def get_user_by_id(id: UUID, db: Session):
    user = db.query(User).filter(User.id == id).first()
    if not user:
        return f"User with id {id} not found"
    return user

def get_company_id_by_user_id(id: UUID, db: Session):
    user = db.query(User).filter(User.id == id).first()
    if not user:
        return f"User with id {id} not found"
    return user.company_id

def get_user_by_company_id(company_id: UUID, db: Session):
    # Query only the id column from users with matching company_id
    user_ids = db.query(User.id).filter(User.company_id == company_id).all()
    if not user_ids:
        return f"User with company id {company_id} not found"

    # Extract the IDs from the result tuples
    result_ids = [user_id[0] for user_id in user_ids]
    print(f"list user ids: {result_ids}")
    return result_ids


def get_all_users(model: UserModel, db: Session):
    users = db.query(User).all()
    if not users:
        return "No users found"
    return users

