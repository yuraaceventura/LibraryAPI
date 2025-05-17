import pytest
from httpx import AsyncClient


@pytest.mark.asyncio(loop_scope="session")
async def test_unauthed_login(client: AsyncClient):
    response = await client.post(
        "/auth/login",
        json={"email": "wrong@example.com", "password": "wrong"}
    )
    assert response.status_code == 401


@pytest.mark.asyncio(loop_scope="session")
async def test_authed_login(auth_client: AsyncClient):
    response = await auth_client.post("/auth/login", json={"email": "user@example.com", "password": "string"})
    assert response.status_code == 200