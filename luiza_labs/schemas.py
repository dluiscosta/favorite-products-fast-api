import pydantic

from uuid import UUID


class ProductSchema(pydantic.BaseModel):
    id: UUID
    price: float
    title: str
    image: str
