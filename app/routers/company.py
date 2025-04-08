from fastapi import APIRouter, Response, Depends
from uuid import UUID
from starlette import status
from database import LocalSession
from models.company import CompanyModel
from sqlalchemy.orm import Session
from schemas import Company
from datetime import datetime
from database import get_db_context
from services import company_service
router = APIRouter(prefix="/company",tags=["company"])

@router.get("", response_model=list[CompanyModel], status_code=status.HTTP_200_OK)
async def all_company(db: Session = Depends(get_db_context)):
    results = db.query(Company).all()
    return results


@router.get("/{company_id}", response_model=list[CompanyModel], status_code=status.HTTP_200_OK)
async def get_company_id(company_id: UUID, db: Session = Depends(get_db_context)):
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
