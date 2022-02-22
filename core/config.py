import os

from pydantic import BaseSettings

from core.exceptions import ConfigurationError


class Config(BaseSettings):
    ENV: str = "production"
    DEBUG: bool = False
    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 8000
    DB_URL: str = "sqlite:///./favorite_products.db"
    LUIZA_LABS_BASE_URL: str = "http://challenge-api.luizalabs.com/api"


class DevelopmentConfig(Config):
    ENV: str = "development"
    DEBUG: bool = True


def get_config():
    env = os.getenv("ENV", "development")
    try:
        return {
            "development": DevelopmentConfig(),
            "production": Config(),
        }[env]
    except KeyError:
        raise ConfigurationError(f"Invalid configured ENV={env}")


config: Config = get_config()
