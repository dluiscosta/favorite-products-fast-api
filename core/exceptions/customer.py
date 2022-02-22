from core.exceptions import HTTPMappedException


class DuplicateEmailError(HTTPMappedException):
    code = 400
    message = "duplicate email or nickname"


class CustomerNotFound(HTTPMappedException):
    code = 404
    message = "customer not found"
