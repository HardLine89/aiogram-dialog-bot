from contextlib import asynccontextmanager
from typing import AsyncGenerator, Any

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from settings.config import Settings


class Database:
    def __init__(self, settings: Settings):
        self._async_engine = create_async_engine(
            url=settings.db_url(),
            pool_pre_ping=False,
            echo=True,
            isolation_level="READ COMMITTED",
        )
        self._async_session = async_sessionmaker(
            bind=self._async_engine,
            expire_on_commit=False,
        )
        self._read_only_async_engine = create_async_engine(
            url=settings.db_url(),
            pool_pre_ping=False,
            isolation_level="AUTOCOMMIT",
        )
        self._read_only_async_session = async_sessionmaker(
            bind=self._read_only_async_engine,
            expire_on_commit=False,
        )

    @asynccontextmanager
    async def get_async_session(self) -> AsyncGenerator[AsyncSession, Any]:
        session: AsyncSession = self._async_session()
        try:
            yield session
        except SQLAlchemyError:
            await session.rollback()
            raise
        finally:
            await session.commit()
            await session.close()

    @asynccontextmanager
    async def get_readonly_async_session(self) -> AsyncGenerator[AsyncSession, Any]:
        session: AsyncSession = self._read_only_async_session()
        try:
            yield session
        except SQLAlchemyError:
            raise
        finally:
            await session.close()

    def get_engine(self):
        return self._async_engine


database = Database(Settings())
