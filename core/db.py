from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from core.config import config

engine = create_engine(config.DB_URL)
SessionLocal = sessionmaker(autocommit=True, autoflush=False, bind=engine)
Base = declarative_base()
