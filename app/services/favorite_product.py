from typing import List

import app.schemas as schemas
import app.models as models

from app.services import BaseService

from luiza_labs.product_fetcher import ProductFetcher
from luiza_labs.schemas import ProductSchema

from core.exceptions.favorite_product import (
    ProductAlreadyFavorite,
    UnexistingCustomer,
    UnexistingProduct,
    FavoriteProductNotFound,
)


class FavoriteProductService(BaseService):

    def get_by_id(self, id: str) -> schemas.FavoriteProductSchema:
        db_favorite_product = self.db_session.query(models.FavoriteProduct) \
                .filter(models.FavoriteProduct.id == id).first()

        if db_favorite_product is not None:
            product_fetcher = ProductFetcher()
            product: ProductSchema = product_fetcher.fetch_product_by_id(
                id=db_favorite_product.product_id
            )
            return schemas.FavoriteProductSchema(
                **db_favorite_product.dict(),
                price=product.price,
                title=product.title,
                image=product.image,
            )
        else:
            raise FavoriteProductNotFound()

    def get_list_by_customer(self, customer_id: str) -> List[schemas.FavoriteProductSchema]:
        db_favorite_products = self.db_session.query(models.FavoriteProduct) \
                .filter(models.FavoriteProduct.customer_id == customer_id)

        product_fetcher = ProductFetcher()
        favorite_products = []
        for db_favorite_product in db_favorite_products:
            # TODO: use concurrent solution
            product: ProductSchema = product_fetcher.fetch_product_by_id(
                id=db_favorite_product.product_id
            )
            favorite_product = schemas.FavoriteProductSchema(
                **db_favorite_product.dict(),
                price=product.price,
                title=product.title,
                image=product.image,
            )
            favorite_products.append(favorite_product)
        return favorite_products

    def create(self, favorite_product: schemas.FavoriteProductCreateSchema):
        db_favorite_product = self.db_session.query(models.FavoriteProduct) \
                .filter(models.FavoriteProduct.customer_id == favorite_product.customer_id) \
                .filter(models.FavoriteProduct.product_id == favorite_product.product_id).all()
        if db_favorite_product:
            raise ProductAlreadyFavorite()

        db_customer = self.db_session.query(models.Customer) \
            .filter(models.Customer.id == favorite_product.customer_id).first()
        if db_customer is None:
            raise UnexistingCustomer()

        product_fetcher = ProductFetcher()
        product: ProductSchema = product_fetcher.fetch_product_by_id(id=favorite_product.product_id)
        if product is None:
            raise UnexistingProduct()

        db_favorite_product = models.FavoriteProduct(**favorite_product.dict())
        self.db_session.add(db_favorite_product)
        self.db_session.flush()
        self.db_session.refresh(db_favorite_product)

        return schemas.FavoriteProductSchema(
            **db_favorite_product.dict(),
            price=product.price,
            title=product.title,
            image=product.image,
        )
