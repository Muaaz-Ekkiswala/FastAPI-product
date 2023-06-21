from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from sqlalchemy.pool import NullPool

from fastapi_product.core.config import settings
from db.database import SessionLocal


def get_db() -> Generator:
    db = SessionLocal()
    db.current_user_id = None
    try:
        yield db
    finally:
        db.close()


def get_session():
    engine = create_engine(settings.DATABASE_URI, poolclass=NullPool)
    Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    return Session()