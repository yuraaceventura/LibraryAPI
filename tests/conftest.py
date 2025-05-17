import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from config.config import settings
from database.base import Base
from main import app


@pytest_asyncio.fixture(loop_scope="session", autouse=True)
async def setup_db():
    engine = create_async_engine(settings.database.get_url())
    async with engine.begin() as conn:
        Base.metadata.schema = "test"
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture
async def client():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
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


@pytest_asyncio.fixture
async def session():
    engine = create_async_engine(settings.database.get_url())
    async_session = async_sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session
        await session.close()

