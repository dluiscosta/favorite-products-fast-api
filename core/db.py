from sqlalchemy import create_engine, inspect
from sqlalchemy.ext.declarative import as_declarative
from sqlalchemy.orm import sessionmaker, scoped_session

from core.config import config

engine = create_engine(config.DB_URL)
session = scoped_session(sessionmaker(bind=engine))


@as_declarative()
class Base:
    def dict(self):
        return {
            c.key: getattr(self, c.key)
            for c in inspect(self).mapper.column_attrs
        }


def get_db_session():
    db_session = session()
    try:
        yield db_session
        db_session.commit()
    finally:
        db_session.close()
