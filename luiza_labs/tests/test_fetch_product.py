import requests_mock
import uuid
import pytest

from luiza_labs.product_fetcher import ProductFetcher
from luiza_labs.sample import read_sample_json
from luiza_labs.schemas import ProductSchema
from core.exceptions.product import ProductNotFound


class TestFetchProductById():

    @requests_mock.Mocker(kw='mocker')
    def test_success(self, **kw):
        PRODUCT_ID = uuid.UUID("1bf0f365-fbdd-4e21-9786-da459d78dd1f")
        kw['mocker'].get(
            ProductFetcher.get_product_url_by_id(PRODUCT_ID),
            json=read_sample_json("product.json"),
        )
        product: ProductSchema = ProductFetcher.fetch_product_by_id(PRODUCT_ID)
        assert product is not None

    @requests_mock.Mocker(kw='mocker')
    def test_not_found(self, **kw):
        PRODUCT_ID = uuid.UUID("1bf0f365-fbdd-4e21-9786-da459d78dd1f")
        kw['mocker'].get(
            ProductFetcher.get_product_url_by_id(PRODUCT_ID),
            json=read_sample_json("not_found.json"),
            status_code=404,
        )
        with pytest.raises(ProductNotFound):
            ProductFetcher.fetch_product_by_id(PRODUCT_ID)
