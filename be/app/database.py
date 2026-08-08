from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from app.config import settings

engine = create_async_engine(
    settings.DATABASE_URL,
    # Supabase's transaction-mode pooler (port 6543) doesn't support prepared
    # statements — asyncpg uses them by default, so disable statement caching.
    connect_args={"statement_cache_size": 0},
)
async_session = async_sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


async def get_db() -> AsyncSession:
    async with async_session() as session:
        yield session
