from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from ..config import settings

engine = create_async_engine(settings.DB_URL)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession)

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

async def init_db():
    # Создаем таблицы при старте
    async with engine.begin() as conn:
        from ..models.base import Base
        await conn.run_sync(Base.metadata.create_all)

async def close_db():
    await engine.dispose()