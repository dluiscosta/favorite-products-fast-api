import pytest
import uuid

from app.services.favorite_product import FavoriteProductService
from app.schemas import (
    CustomerCreateSchema,
    FavoriteProductCreateSchema,
    FavoriteProductSchema,
)
from app.models import Customer, FavoriteProduct

from core.exceptions.favorite_product import ProductAlreadyFavorite, UnexistingCustomer

from luiza_labs.sample import read_sample_json
from luiza_labs.schemas import ProductSchema


class TestFavoriteProductService():

    dummy_customer_create = CustomerCreateSchema(
        full_name="Daniel Luis Costa",
        email="dluiscosta@gmail.com",
        password=123456,
    )

    def __create_dummy_customer(self, db_session) -> Customer:
        db_customer = Customer(**self.dummy_customer_create.dict())
        db_session.add(db_customer)
        db_session.flush()
        db_session.refresh(db_customer)
        return db_customer

    def test_get_by_id(self, mocker, db_session):
        db_customer = self.__create_dummy_customer(db_session)

        product_id = uuid.uuid4()
        favorite_product_create = FavoriteProductCreateSchema(
            product_id=product_id,
            customer_id=db_customer.id,
        )
        db_favorite_product = FavoriteProduct(**favorite_product_create.dict())
        db_session.add(db_favorite_product)
        db_session.flush()
        db_session.refresh(db_favorite_product)

        product = ProductSchema(**read_sample_json('product.json'))
        product.id = product_id
        mocker.patch(
            'luiza_labs.product_fetcher.ProductFetcher.fetch_product_by_id',
            return_value=product
        )

        service = FavoriteProductService(db_session=db_session)
        favorite_product = service.get_by_id(id=db_favorite_product.id)
        assert favorite_product is not None
        assert favorite_product.dict() == {
            **db_favorite_product.dict(),
            'price': product.price,
            'title': product.title,
            'image': product.image,
        }

    def test_get_list_by_customer(self, mocker, db_session):
        db_customer = self.__create_dummy_customer(db_session)
        product = ProductSchema(**read_sample_json('product.json'))

        db_favorite_products = []
        for i in range(3):
            product_id = uuid.uuid4()
            favorite_product_create = FavoriteProductCreateSchema(
                product_id=product_id,
                customer_id=db_customer.id,
            )

            product.id = product_id
            mocker.patch(
                'luiza_labs.product_fetcher.ProductFetcher.fetch_product_by_id',
                return_value=product
            )

            db_favorite_product = FavoriteProduct(**favorite_product_create.dict())
            db_session.add(db_favorite_product)
            db_session.flush()
            db_session.refresh(db_favorite_product)
            db_favorite_products.append(db_favorite_product)

        service = FavoriteProductService(db_session=db_session)
        favorite_products = service.get_list_by_customer(customer_id=db_customer.id)
        assert len(favorite_products) == 3

        for db_favorite_product in db_favorite_products:
            assert {
                **db_favorite_product.dict(),
                'price': product.price,
                'title': product.title,
                'image': product.image,
            } in favorite_products

    def test_create(self, mocker, db_session):
        db_customer = self.__create_dummy_customer(db_session)

        product_id = uuid.uuid4()
        service = FavoriteProductService(db_session=db_session)
        favorite_product_create = FavoriteProductCreateSchema(
            product_id=product_id,
            customer_id=db_customer.id,
        )

        product = ProductSchema(**read_sample_json('product.json'))
        product.id = product_id
        fetch_product_mocker = mocker.patch(
            'luiza_labs.product_fetcher.ProductFetcher.fetch_product_by_id',
            return_value=product
        )
        favorite_product = service.create(favorite_product_create)

        assert isinstance(favorite_product, FavoriteProductSchema)

        fetch_product_mocker.assert_called_once_with(id=product_id)
        assert favorite_product == FavoriteProductSchema(
            **favorite_product_create.dict(),
            id=favorite_product.id,
            price=product.price,
            title=product.title,
            image=product.image,
        )

        db_favorite_product = db_session.query(FavoriteProduct) \
            .filter(FavoriteProduct.id == favorite_product.id).first()
        assert db_favorite_product is not None
        assert db_favorite_product.dict() == {
            **favorite_product_create.dict(),
            'id': db_favorite_product.id,
        }

    def test_create_fails_already_favorite(self, db_session):
        db_customer = self.__create_dummy_customer(db_session)
        favorite_product_create = FavoriteProductCreateSchema(
            product_id=uuid.uuid4(),
            customer_id=db_customer.id,
        )
        db_favorite_product = FavoriteProduct(**favorite_product_create.dict())
        db_session.add(db_favorite_product)

        service = FavoriteProductService(db_session=db_session)
        with pytest.raises(ProductAlreadyFavorite):
            service.create(favorite_product_create)

    def test_create_fails_unexisting_customer(self, db_session):
        favorite_product_create = FavoriteProductCreateSchema(
            product_id=uuid.uuid4(),
            customer_id=uuid.uuid4(),
        )
        service = FavoriteProductService(db_session=db_session)
        with pytest.raises(UnexistingCustomer):
            service.create(favorite_product_create)
