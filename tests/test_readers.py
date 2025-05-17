import pytest
from starlette import status


@pytest.mark.asyncio(loop_scope="session")
class TestReadersEndpoints:

    async def test_get_readers(self, auth_client):
        response = await auth_client.get("/readers")
        assert response.status_code == status.HTTP_200_OK
        assert isinstance(response.json(), list)


    @pytest.mark.parametrize("name, email, response_status", [
        ("John Doe", "user@example.com", 200),
        ("John Doe", "user@example.com", 409),
    ])
    async def test_create_reader(self, name, email, response_status, auth_client):
        payload = {
            "name": name,
            "email": email,
        }
        response = await auth_client.post("/readers", json=payload)
        if response_status == 409:
            reader_id = response.json().get("id")
            response = await auth_client.post("/readers", json=payload)
            assert response.status_code == response_status
            await auth_client.delete(f"/readers/{reader_id}")
        else:
            assert response.status_code == response_status
            reader_id = response.json().get("id")
            await auth_client.delete(f"/readers/{reader_id}")

    async def test_get_reader_by_id(self, auth_client):
        payload = {
            "name" : "John Doe",
            "email": "user@example.com"
        }
        response = await auth_client.post("/readers", json=payload)
        reader_id = response.json().get("id")

        response = await auth_client.get(f"/readers/{reader_id}")

        assert response.status_code == status.HTTP_200_OK
        assert response.json()["id"] == reader_id
        await auth_client.delete(f"/readers/{reader_id}")



    async def test_delete_reader_correct(self, auth_client):
        payload = {
            "name": "John Doe",
            "email": "user@example.com"
        }
        response = await auth_client.post("/readers", json=payload)
        reader_id = response.json().get("id")

        response = await auth_client.delete(f"/readers/{reader_id}")

        assert response.status_code == status.HTTP_200_OK


    async def test_delete_reader_incorrect(self, auth_client):
        response = await auth_client.delete("/readers/999999")
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json()["detail"] == "Couldn't find this reader"


