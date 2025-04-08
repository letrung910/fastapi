from uuid import UUID
from sqlalchemy.orm import Session
from schemas import Company
from models.company import CompanyModel
from datetime import datetime

def get_company_id(id: UUID, db: Session):
    query = db.query(Company).filter(Company.id == id).first()
    return query


def create_company(model: CompanyModel, db: Session):
    company = Company(**model.dict())
    company.created_at = datetime.utcnow()
    db.add(company)
    db.commit()
    return f"Create {model.name} sucessfull"

def update_company(company_id: UUID, model: CompanyModel, db: Session):
    company = get_company_id(company_id, db)
    if company is None:
        return False
    company.description = model.description
    company.mode = model.mode
    company.name = model.name
    company.rating = model.rating
    company.updated_at = datetime.utcnow()

    db.add(company)
    db.commit()
    # db.refresh(company)
    return f"Update {company_id} complete"


def delete_company(company_id: UUID, model: CompanyModel, db: Session):
    company = get_company_id(company_id, db)
    if company is None:
        return False
