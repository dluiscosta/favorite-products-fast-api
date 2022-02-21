import uuid

from sqlalchemy import String, Column, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.schema import UniqueConstraint

from core.db import Base


def generate_uuid():
    return str(uuid.uuid4())


class Customer(Base):
    __tablename__ = 'customers'

    id = Column(String, primary_key=True, default=generate_uuid)
    full_name = Column(String)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    favorite_products = relationship('FavoriteProduct')


class FavoriteProduct(Base):
    __tablename__ = 'favorite_products'

    id = Column(String, primary_key=True, default=generate_uuid)
    product_id = Column(String)
    customer_id = Column(String, ForeignKey("customers.id"))
    __table_args__ = (
        UniqueConstraint('product_id', 'customer_id', name='_product_customer_uc'),
    )
