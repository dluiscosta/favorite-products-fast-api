import requests

from uuid import UUID

from core.exceptions.product import ProductNotFound
from core.config import config
from luiza_labs.schemas import ProductSchema


class ProductFetcher():

    @staticmethod
    def get_product_url_by_id(id: UUID):
        return f"{config.LUIZA_LABS_BASE_URL}/product/{str(id)}/"

    @classmethod
    def fetch_product_by_id(cls, id: UUID) -> ProductSchema:
        response = requests.get(url=cls.get_product_url_by_id(id))

        try:
            response.raise_for_status()
        except requests.HTTPError as err:
            if err.response.status_code == 404:
                raise ProductNotFound()
            else:
                raise err

        return ProductSchema(**response.json())
