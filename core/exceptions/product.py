from core.exceptions import HTTPMappedException


class ProductNotFound(HTTPMappedException):
    code = 400
    message = "product not found"
