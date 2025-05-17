import pytest
from starlette import status


@pytest.mark.asyncio(loop_scope="session")
class TestBooksEndpoints:

    async def test_get_books_empty(self, auth_client):
        response = await auth_client.get("/books/")
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == []



    async def test_create_book_success(self, auth_client):
        payload = {
            "title": "New Title",
            "author": "Author X",
            "published_at": 2023,
            "ISBN": "ISBN123",
            "available": 1
        }
        response = await auth_client.post("/books/", json=payload)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["title"] == payload["title"]
        assert data["author"] == payload["author"]
        book_id = data["id"]
        await auth_client.delete(f"/books/{book_id}")



    @pytest.mark.parametrize("book_id, expected_status", [
        (1, status.HTTP_200_OK),
        (999, status.HTTP_404_NOT_FOUND),
    ])
    async def test_get_book_by_id(self, auth_client, book_id, expected_status):
        payload = {
            "title": "Lookup Book",
            "author": "Author Y",
            "published_at": 2024,
            "ISBN": "ISBN456",
            "available": 1
        }
        create = await auth_client.post("/books/", json=payload)
        if create.status_code == 200:
            book_id = create.json()["id"]
            get_ok = await auth_client.get(f"/books/{book_id}")
            assert get_ok.status_code == status.HTTP_200_OK
            assert get_ok.json()["id"] == book_id
        else:
            error = create.json()
            assert "detail" in error


        get_not = await auth_client.get("/books/9999")
        assert get_not.status_code == status.HTTP_404_NOT_FOUND
        await auth_client.delete(f"/books/{book_id}")



    @pytest.mark.parametrize("book_id, expected_status", [
        (1, status.HTTP_200_OK),
        (999, status.HTTP_404_NOT_FOUND),
    ])
    async def test_delete_book(self, auth_client, book_id, expected_status):
        payload = {
            "title": "To Delete",
            "author": "Author Z",
            "published_at": 2025,
            "ISBN": "ISBN789",
            "available": 1
        }
        book_id = (await auth_client.post("/books/", json=payload)).json()["id"]

        del_ok = await auth_client.delete(f"/books/{book_id}")
        assert del_ok.status_code == status.HTTP_200_OK
        if del_ok.status_code == status.HTTP_200_OK:
            data = del_ok.json()
            assert "id" in data
        else:
            error = del_ok.json()
            assert "detail" in error


        # Повторное удаление той же → 404
        del_again = await auth_client.delete(f"/books/{book_id}")
        assert del_again.status_code == status.HTTP_404_NOT_FOUND



    @pytest.mark.parametrize("update_data, expected_status", [
        ({"title": "Updated"}, status.HTTP_200_OK),
        ({}, status.HTTP_409_CONFLICT),
    ])
    async def test_update_book(self, auth_client, update_data, expected_status):
        payload = {
            "title": "To Delete",
            "author": "Author Z",
            "published_at": 2025,
            "ISBN": "unique ISBN",
            "available": 1
        }
        response = (await auth_client.post("/books/", json=payload))
        body = response.json()
        book_id = body["id"]
        response = await auth_client.patch(
            f"/books/{book_id}",
            json=update_data
        )
        assert response.status_code == expected_status
        if expected_status == status.HTTP_200_OK:
            book = response.json()
            for key, value in update_data.items():
                assert book[key] == value
        await auth_client.delete(f"/books/{book_id}")

