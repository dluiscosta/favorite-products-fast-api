from typing import List

import app.schemas as schemas
import app.models as models

from app.services import BaseService
from app.services.favorite_product import FavoriteProductService

from core.exceptions.customer import DuplicateEmailError, CustomerNotFound


class CustomerService(BaseService):

    def get_by_id(self, id: str) -> schemas.CustomerSchema:
        db_customer = self.db_session.query(models.Customer) \
                .filter(models.Customer.id == id).first()
        if db_customer is not None:
            customer = schemas.CustomerSchema(**db_customer.dict())
            favorite_product_service = FavoriteProductService(self.db_session)
            customer.favorite_products = favorite_product_service.get_list_by_customer(
                customer_id=customer.id
            )
            return customer
        else:
            raise CustomerNotFound()

    def get_by_email(self, email: str) -> schemas.CustomerSchema:
        db_customer = self.db_session.query(models.Customer) \
                .filter(models.Customer.email == email).first()
        if db_customer is not None:
            return schemas.CustomerSchema.from_orm(db_customer)

    def get_list(self) -> List[schemas.CustomerSchema]:
        return [
            schemas.CustomerSchema.from_orm(db_customer)
            for db_customer in self.db_session.query(models.Customer)
        ]

    def create(self, customer: schemas.CustomerCreateSchema) -> schemas.CustomerSchema:
        if self.get_by_email(customer.email) is not None:
            raise DuplicateEmailError()

        db_customer = models.Customer(**customer.dict())
        self.db_session.add(db_customer)
        self.db_session.flush()
        self.db_session.refresh(db_customer)
        return schemas.CustomerSchema.from_orm(db_customer)
