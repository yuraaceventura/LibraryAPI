import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy import delete, text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from config.config import settings
from database.base import Base
from main import app


@pytest_asyncio.fixture(loop_scope="session", autouse=True)
async def setup_db():
    engine = create_async_engine(settings.database.get_url_test())
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


@pytest_asyncio.fixture(autouse=True, scope="function")
async def truncate_tables():
    engine = create_async_engine(settings.database.get_url_test())
    async with engine.begin() as conn:
        for table in reversed(Base.metadata.sorted_tables):
            await conn.execute(text(f'TRUNCATE "{table.name}" RESTART IDENTITY CASCADE;'))
    yield


@pytest_asyncio.fixture
async def db_session():
    engine = create_async_engine(settings.database.get_url_test())
    session_maker = async_sessionmaker(
        engine, expire_on_commit=False
    )
    async with session_maker() as session:
        yield session


@pytest_asyncio.fixture
async def client():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test", follow_redirects=True) as client:
        yield client


@pytest_asyncio.fixture
async def auth_client(client: AsyncClient):
    await client.post(
        "/auth/register",
        json={"email": "user@example.com", "password": "string"}
    )

    login_response = await client.post(
        "/auth/login",
        json={"email": "user@example.com", "password": "string"}
    )

    client.cookies = login_response.cookies
    return client

