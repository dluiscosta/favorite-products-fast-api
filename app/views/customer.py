import uuid

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

import app.schemas as schemas

from app.services.customer import CustomerService
from core.db import get_db_session


customer_router = APIRouter(prefix="/customer")


@customer_router.get("/{customer_id}", response_model=schemas.CustomerSchema)
def read_customer(customer_id: uuid.UUID, db: Session = Depends(get_db_session)):
    customer_service = CustomerService(db_session=db)
    return customer_service.get_by_id(id=customer_id)


@customer_router.post("/", response_model=schemas.CustomerSchema)
def create_customer(customer: schemas.CustomerCreateSchema, db: Session = Depends(get_db_session)):
    customer_service = CustomerService(db_session=db)
    return customer_service.create(customer=customer)
