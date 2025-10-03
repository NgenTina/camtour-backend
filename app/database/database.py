from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy.pool import QueuePool
from app.core.config import settings
from sqlalchemy.ext.asyncio import AsyncSession
import os
from sqlalchemy import create_engine

database_url = settings.ephemeral_database_url if settings.debug else settings.database_url

# Detect if running under Alembic migration
if os.environ.get("ALEMBIC_MIGRATION", "0") == "1":
    # Use sync engine for Alembic
    engine = create_engine(
        database_url.replace("+asyncpg", "+psycopg2"),
        poolclass=QueuePool,
        pool_size=20,
        max_overflow=30,
        pool_pre_ping=True,
        pool_recycle=300,
    )
    SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)
else:
    # Use async engine for app
    engine = create_async_engine(
        database_url,
        poolclass=QueuePool,
        pool_size=20,
        max_overflow=30,
        pool_pre_ping=True,
        pool_recycle=300,
    )
    AsyncSessionLocal = async_sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False
    )


class Base(DeclarativeBase):
    pass

# Dependency to get database session


async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
