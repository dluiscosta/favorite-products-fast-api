from core.exceptions import HTTPMappedException


class DuplicateEmailError(HTTPMappedException):
    code = 400
    message = "duplicate email or nickname"
