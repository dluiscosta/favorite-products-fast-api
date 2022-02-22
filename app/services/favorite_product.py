import app.schemas as schemas
import app.models as models

from app.services import BaseService
from app.services.customer import CustomerService
from core.exceptions.favorite_product import ProductAlreadyFavorite, UnexistingCustomer


class FavoriteProductService(BaseService):

    def get_by_id(self, id: str) -> schemas.FavoriteProductSchema:
        db_favorite_product = self.db_session.query(models.FavoriteProduct) \
                .filter(models.FavoriteProduct.id == id).first()
        if db_favorite_product is not None:
            return schemas.FavoriteProductSchema.from_orm(db_favorite_product)

    def get_list_by_customer(self, customer_id: str) -> schemas.FavoriteProductSchema:
        db_favorite_products = self.db_session.query(models.FavoriteProduct) \
                .filter(models.FavoriteProduct.customer_id == customer_id)
        return [
            schemas.FavoriteProductSchema.from_orm(db_favorite_product)
            for db_favorite_product in db_favorite_products
        ]

    def create(self, favorite_product: schemas.FavoriteProductCreateSchema):
        db_favorite_product = self.db_session.query(models.FavoriteProduct) \
                .filter(models.FavoriteProduct.customer_id == favorite_product.customer_id) \
                .filter(models.FavoriteProduct.product_id == favorite_product.product_id).all()
        if db_favorite_product:
            raise ProductAlreadyFavorite()

        customer_service = CustomerService(db_session=self.db_session)
        customer = customer_service.get_by_id(favorite_product.customer_id)
        if customer is None:
            raise UnexistingCustomer()

        # TODO: check product id exists against external API

        db_favorite_product = models.FavoriteProduct(**favorite_product.dict())
        self.db_session.add(db_favorite_product)
        self.db_session.flush()
        self.db_session.refresh(db_favorite_product)
        return schemas.FavoriteProductSchema.from_orm(db_favorite_product)
