from fastapi import FastAPI

from app.views import root_router
from core.config import config


def init_routers(app: FastAPI) -> None:
    app.include_router(root_router)


def create_app() -> FastAPI:
    app = FastAPI(
        title="Favorite Products",
        description="Check or update a customers favorite products.",
        version="0.0.0",
        docs_url=None if config.ENV == "production" else "/docs",
        redoc_url=None if config.ENV == "production" else "/redoc",
    )
    init_routers(app=app)
    return app


app = create_app()
