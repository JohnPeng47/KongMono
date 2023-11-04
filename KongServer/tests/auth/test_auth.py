import pytest
from async_asgi_testclient import TestClient
from fastapi import status

@pytest.mark.asyncio
async def test_register(client: TestClient) -> None:
    resp = await client.post(
        "/auth/users",
        json={
            "email": "email@fake.com",
            "password": "123Aa!",
        },
    )
    resp_json = resp.json()

    assert resp.status_code == status.HTTP_201_CREATED
    assert resp_json == {"email": "email@fake.com"}