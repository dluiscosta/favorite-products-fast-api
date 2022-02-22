import uuid

from sqlalchemy import String, Column, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.schema import UniqueConstraint
from sqlalchemy_utils import UUIDType

from core.db import Base, engine


class Customer(Base):
    __tablename__ = 'customers'

    id = Column(UUIDType, primary_key=True, default=uuid.uuid4)
    full_name = Column(String)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    favorite_products = relationship('FavoriteProduct')


class FavoriteProduct(Base):
    __tablename__ = 'favorite_products'

    id = Column(UUIDType, primary_key=True, default=uuid.uuid4)
    product_id = Column(UUIDType)
    customer_id = Column(UUIDType, ForeignKey("customers.id"))
    __table_args__ = (
        UniqueConstraint('product_id', 'customer_id', name='_product_customer_uc'),
    )


Base.metadata.create_all(bind=engine)
