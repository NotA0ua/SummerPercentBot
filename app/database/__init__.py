from contextlib import asynccontextmanager
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app import DATABASE_URL
from .models import Base
from .users import UsersOperations


class Database:
    def __init__(self):
        self.engine = create_async_engine(DATABASE_URL)
        self.session = sessionmaker(
            self.engine, class_=AsyncSession, expire_on_commit=False
        )

    async def init_db(self) -> None:
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    @asynccontextmanager
    async def get_session(self) -> AsyncGenerator[AsyncSession]:
        async with self.session() as session:
            yield session

    async def dispose(self) -> None:
        await self.engine.dispose()
