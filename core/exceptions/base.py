class ConfigurationError(ValueError):
    """
    Configuration error from environment variables set with invalid values.
    """
    def __init__(self, message):
        super().__init__(
            f"Configuration error, check environment variables. {message.capitalize()}."
        )
