from sqlalchemy import Integer, String, Column, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.schema import UniqueConstraint

from core.db import Base


class Customer(Base):
    __tablename__ = 'customers'

    id = Column(Integer, primary_key=True)
    full_name = Column(String)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    favorite_products = relationship('FavoriteProduct')


class FavoriteProduct(Base):
    __tablename__ = 'favorite_products'

    id = Column(Integer, primary_key=True)
    product_id = Column(Integer)
    customer_id = Column(Integer, ForeignKey("customers.id"))
    __table_args__ = (
        UniqueConstraint('product_id', 'customer_id', name='_product_customer_uc'),
    )
