from fastapi import APIRouter, Response, Depends, HTTPException
from uuid import UUID
from starlette import status
from database import LocalSession
from models.company import CompanyModel
from sqlalchemy.orm import Session
from schemas import Company, User
from datetime import datetime
from database import get_db_context
from services import company_service, auth_service
router = APIRouter(prefix="/company",tags=["company"])

@router.get("", response_model=list[CompanyModel], status_code=status.HTTP_200_OK)
async def all_company(
        db: Session = Depends(get_db_context),
        user: User = Depends(auth_service.token_interceptor)):

    if not User.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to access this resource",
        )
    results = db.query(Company).all()
    return results


@router.get("/{company_id}", response_model=list[CompanyModel], status_code=status.HTTP_200_OK)
async def get_company_id(
        company_id: UUID,
        user: User = Depends(auth_service.token_interceptor),
        db: Session = Depends(get_db_context)):
    if not User.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to access this resource",
        )
    results = db.query(Company).filter(Company.id == company_id)
    return results


@router.post("/createcompany", status_code=status.HTTP_201_CREATED)
async def create_company(request: CompanyModel , db: Session = Depends(get_db_context)):
    results = company_service.create_company(request, db)
    return results

@router.put("/updatecompany/{company_id}", status_code=status.HTTP_200_OK)
async def update_company(company_id: UUID, request: CompanyModel, db: Session = Depends(get_db_context)):
    results = company_service.update_company(company_id, request, db)
    return results
