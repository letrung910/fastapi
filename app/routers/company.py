from fastapi import APIRouter, Response, Depends
from uuid import UUID
from starlette import status
from database import LocalSession
from models.company import CompanyModel
from sqlalchemy.orm import Session
from schemas.company import Company
from datetime import datetime
from database import get_db_context

router = APIRouter(prefix="/company",tags=["company"])

@router.get("", response_model=list[CompanyModel], status_code=status.HTTP_200_OK)
async def get_company(db: Session = Depends(get_db_context)):
    return db.query(Company).all()


@router.get("/{company_id}")
async def get_company_id(company_id: UUID):
    return "company"

@router.post("/createcompany", status_code=status.HTTP_201_CREATED)
async def create_company(request: CompanyModel, db: Session = Depends(get_db_context)):
    company = Company(**request.dict())
    company.created_at = datetime.utcnow()
    db.add(company)
    db.commit()
