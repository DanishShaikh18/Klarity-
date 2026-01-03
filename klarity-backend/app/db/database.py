# app/db/database.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# SQLite file in project root: ./klarity.db
SQLALCHEMY_DATABASE_URL = "sqlite:///./klarity.db"

# For SQLite, we need this flag for multithreading (FastAPI)
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Session factory – we’ll use this in routes to talk to DB
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for all ORM models (Chat, Message, Document)
Base = declarative_base()


def get_db():
    """
    FastAPI dependency: gives a database session to a request
    and makes sure it's closed afterwards.
    Usage in routes later:

        from fastapi import Depends
        from app.db.database import get_db

        def my_route(db: Session = Depends(get_db)):
            ...

    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
