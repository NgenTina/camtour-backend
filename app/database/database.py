from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.pool import QueuePool
from app.core.config import settings

database_url = settings.ephemeral_database_url if settings.debug else settings.database_url

# Create async engine
engine = create_async_engine(
    settings.database_url,
    poolclass=QueuePool,
    pool_size=20,
    max_overflow=30,
    pool_pre_ping=True,
    pool_recycle=300,
)

# Create async session
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=async_sessionmaker,
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
