from typing import AsyncGenerator
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from src.config import Config


engine = create_async_engine(
    url=Config.DATABASE_URL,
    echo=True,
    connect_args={"ssl": "require"}
)

async def init_db():
    async with engine.begin() as conn:
        from src.books.models import Book

        await conn.run_sync(SQLModel.metadata.create_all)

async_session_maker = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session