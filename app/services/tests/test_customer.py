import pytest

from app.services.customer import CustomerService
from app.schemas import CustomerCreateSchema, CustomerSchema
from app.models import Customer
from core.exceptions.customer import DuplicateEmailError


class TestCustomerService():

    dummy_customer_create = CustomerCreateSchema(
        full_name="Daniel Luis Costa",
        email="dluiscosta@gmail.com",
        password=123456,
    )
    dummy_customer_create_2 = CustomerCreateSchema(
        full_name="John Doe",
        email="john.doe@gmail.com",
        password=654321,
    )

    def test_get_by_email(self, db_session):
        db_customer = Customer(**self.dummy_customer_create.dict())
        db_session.add(db_customer)

        service = CustomerService(db_session=db_session)
        customer = service.get_by_email(email=self.dummy_customer_create.email)
        assert customer is not None
        assert CustomerSchema.from_orm(db_customer) == customer

    def test_get_by_id(self, db_session):
        db_customer = Customer(**self.dummy_customer_create.dict())
        db_session.add(db_customer)
        db_session.flush()
        db_session.refresh(db_customer)

        service = CustomerService(db_session=db_session)
        customer = service.get_by_id(id=db_customer.id)
        assert customer is not None
        assert CustomerSchema.from_orm(db_customer) == customer

    def test_get_list(self, db_session):
        db_customer_1 = Customer(**self.dummy_customer_create.dict())
        db_customer_2 = Customer(**self.dummy_customer_create_2.dict())
        db_session.add(db_customer_1)
        db_session.add(db_customer_2)

        service = CustomerService(db_session=db_session)
        customers = service.get_list()
        assert len(customers) == 2
        for db_customer in [db_customer_1, db_customer_2]:
            assert CustomerSchema.from_orm(db_customer) in customers

    def test_create(self, db_session):
        service = CustomerService(db_session=db_session)
        customer = service.create(self.dummy_customer_create)
        assert isinstance(customer, CustomerSchema)

        db_customer = db_session.query(Customer).filter(Customer.id == str(customer.id)).first()
        assert db_customer is not None
        assert CustomerSchema.from_orm(db_customer) == CustomerSchema(
            **self.dummy_customer_create.dict(), id=db_customer.id
        )

    def test_create_fails_duplicate_email(self, db_session):
        db_customer = Customer(**self.dummy_customer_create.dict())
        db_session.add(db_customer)

        service = CustomerService(db_session=db_session)
        with pytest.raises(DuplicateEmailError):
            service.create(self.dummy_customer_create)
