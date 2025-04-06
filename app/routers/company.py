from fastapi import APIRouter, status, Response
from uuid import UUID
from models.company import CompanyModel

router = APIRouter(prefix="/company",tags=["company"])

@router.get("/listcompany", status_code=status.HTTP_200_OK)
async def list_company() -> str:
    return "List Company"

@router.get("/{company_id}")
async def get_company(company_id: UUID):
    return "company"

@router.post("/createcompany", status_code=status.HTTP_201_CREATED)
async def create_company(request: CompanyModel):
    return "create company"