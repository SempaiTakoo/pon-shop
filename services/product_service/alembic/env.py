import os
import sys
from logging.config import fileConfig

# Добавляем путь к проекту в PYTHONPATH
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.ext.asyncio import create_async_engine
from alembic import context
import asyncio

# Импортируем Base из нашего проекта
from app.models.base import Base
target_metadata = Base.metadata

def run_migrations_online():
    connectable = create_async_engine(context.config.get_main_option("sqlalchemy.url"))

    async def run_migrations(connection):
        await connection.run_sync(
            lambda sync_conn: context.run(
                migrations=sync_conn,
                target_metadata=target_metadata
            )
        )

    asyncio.run(run_migrations(connectable))

fileConfig(context.config.config_file_name)