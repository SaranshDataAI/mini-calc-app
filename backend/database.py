"""
Database connection setup.

Why SQLite: zero setup, it's just a file on disk. Good enough for
learning — we can swap to Postgres later without changing much else,
since SQLAlchemy abstracts the underlying database.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "sqlite:///./calculator.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},  # needed for SQLite + FastAPI
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """FastAPI dependency — gives each request its own DB session,
    and always closes it afterward, even if the request fails."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
