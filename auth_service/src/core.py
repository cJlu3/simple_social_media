from sqlalchemy import create_engine, inspect
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import sessionmaker, DeclarativeBase

from src.config import Settings

sync_engine = create_engine(
    url=Settings.DB_SYNC_URL,
)
sync_session_factory = sessionmaker(sync_engine)

async_engine = create_async_engine(
    url=Settings.DB_ASYNC_URL,
)
async_session_factory = async_sessionmaker(async_engine)

class Base(DeclarativeBase):
    pass

def tables_check():
    inspector = inspect(sync_engine)
    existing_tables = inspector.get_table_names()

    if not existing_tables:
        Base.metadata.create_all(sync_engine)
