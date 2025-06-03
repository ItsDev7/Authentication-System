# database.py
"""
Module for database configuration and session management.
Sets up the asynchronous SQLAlchemy engine and session local.
"""

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from .config import settings

# Create an asynchronous database engine
# echo=True will log SQL statements to the console (useful for debugging)
engine = create_async_engine(settings.DATABASE_URL, echo=True)

# Create a configured "Session" class
# use class_=AsyncSession for async sessions
# expire_on_commit=False prevents objects from being expired after commit
SessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

# Define a base class for declarative models
class Base(DeclarativeBase):
    pass

# Dependency to get an asynchronous database session
async def get_db():
    """Provides an asynchronous database session for FastAPI dependencies."""
    db = SessionLocal()
    try:
        yield db
    finally:
        await db.close()