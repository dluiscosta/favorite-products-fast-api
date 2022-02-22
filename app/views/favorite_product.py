import uuid

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

import app.schemas as schemas

from app.services.favorite_product import FavoriteProductService
from core.db import get_db_session


favorite_product_router = APIRouter(prefix="/favorite_product")


@favorite_product_router.get("/{favorite_product_id}", response_model=schemas.FavoriteProductSchema)
def read_favorite_product(favorite_product_id: uuid.UUID, db: Session = Depends(get_db_session)):
    favorite_product_service = FavoriteProductService(db_session=db)
    return favorite_product_service.get_by_id(id=favorite_product_id)


@favorite_product_router.post("/", response_model=schemas.FavoriteProductSchema)
def create_favorite_product(
    favorite_product: schemas.FavoriteProductCreateSchema,
    db: Session = Depends(get_db_session)
):
    favorite_product_service = FavoriteProductService(db_session=db)
    return favorite_product_service.create(favorite_product=favorite_product)
