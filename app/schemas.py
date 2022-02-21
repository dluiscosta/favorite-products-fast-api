import pydantic

from uuid import UUID
from typing import List


class FavoriteProductBaseSchema(pydantic.BaseModel):
    product_id: UUID
    customer_id: UUID


class FavoriteProductCreateSchema(FavoriteProductBaseSchema):
    pass


class FavoriteProductSchema(FavoriteProductBaseSchema):
    id: UUID
    price: float
    title: str
    image: str

    class Config:
        orm_mode = True


class CustomerBaseSchema(pydantic.BaseModel):
    full_name: str
    email: pydantic.EmailStr

    @pydantic.validator('full_name')
    def validate_and_title_full_name(cls, full_name):
        if full_name == "":
            raise ValueError('must not be empty')
        return full_name.title()


class CustomerCreateSchema(CustomerBaseSchema):
    password: str


class CustomerSchema(CustomerBaseSchema):
    id: UUID
    favorite_products: List[FavoriteProductSchema] = []

    class Config:
        orm_mode = True
