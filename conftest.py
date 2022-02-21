import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


from core import db


@pytest.fixture(scope='session')
def db_engine():
    """Yield a SQLAlchemy engine which is suppressed after the test session"""
    engine_ = create_engine("sqlite:///:memory:", echo=True)
    db.Base.metadata.create_all(bind=engine_)

    yield engine_

    engine_.dispose()


@pytest.fixture(scope='session')
def db_session_factory(db_engine):
    """Return a SQLAlchemy scoped session factory"""
    return scoped_session(sessionmaker(bind=db_engine))


@pytest.fixture(scope='function')
def db_session(db_session_factory):
    """Yield a SQLAlchemy connection which is rollbacked after the test"""
    session_ = db_session_factory()

    yield session_

    session_.rollback()
    session_.close()
