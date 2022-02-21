from http import HTTPStatus


class ConfigurationError(ValueError):
    """
    Configuration error from environment variables set with invalid values.
    """
    def __init__(self, message=None):
        super().__init__(
            "Configuration error, check environment variables." +
            f" {message.capitalize()}." if message else ""
        )


class HTTPMappedException(Exception):
    code = HTTPStatus.BAD_GATEWAY
    message = HTTPStatus.BAD_GATEWAY.description

    def __init__(self, message=None):
        if message:
            self.message = message
