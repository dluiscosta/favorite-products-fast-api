from core.exceptions import HTTPMappedException


class ProductAlreadyFavorite(HTTPMappedException):
    code = 400
    message = "product already a favorite of this customer"


class UnexistingCustomer(HTTPMappedException):
    code = 400
    message = "customer does not exist"
