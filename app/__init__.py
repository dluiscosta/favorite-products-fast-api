from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.views import root_router
from app.views.customer import customer_router
from app.views.favorite_product import favorite_product_router
from core.config import config
from core.exceptions import HTTPMappedException


def init_routers(app: FastAPI) -> None:
    app.include_router(root_router)
    app.include_router(customer_router)
    app.include_router(favorite_product_router)


def init_listeners(app: FastAPI) -> None:
    @app.exception_handler(HTTPMappedException)
    async def custom_exception_handler(request: Request, exc: HTTPMappedException):
        return JSONResponse(
            status_code=exc.code,
            content={"message": exc.message},
        )


def create_app() -> FastAPI:
    app = FastAPI(
        title="Favorite Products",
        description="Check or update a customers favorite products.",
        version="0.0.0",
        docs_url=None if config.ENV == "production" else "/docs",
        redoc_url=None if config.ENV == "production" else "/redoc",
    )
    init_routers(app=app)
    init_listeners(app=app)
    return app


app = create_app()
