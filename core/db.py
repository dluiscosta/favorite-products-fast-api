from sqlalchemy import create_engine, inspect
from sqlalchemy.ext.declarative import as_declarative
from sqlalchemy.orm import sessionmaker

from core.config import config

engine = create_engine(config.DB_URL)
SessionLocal = sessionmaker(autocommit=True, autoflush=False, bind=engine)


@as_declarative()
class Base:
    def dict(self):
        return {
            c.key: getattr(self, c.key)
            for c in inspect(self).mapper.column_attrs
        }
