"""Tests for the items CRUD API."""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_list_items_empty(client: AsyncClient) -> None:
    response = await client.get("/api/v1/items")
    assert response.status_code == 200
    data = response.json()
    assert data["items"] == []
    assert data["total"] == 0


@pytest.mark.asyncio
async def test_create_item(client: AsyncClient) -> None:
    payload = {"title": "Test item", "description": "A description"}
    response = await client.post("/api/v1/items", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test item"
    assert data["description"] == "A description"
    assert "id" in data
    assert "created_at" in data


@pytest.mark.asyncio
async def test_get_item(client: AsyncClient) -> None:
    # Create first
    create_resp = await client.post("/api/v1/items", json={"title": "My item"})
    item_id = create_resp.json()["id"]

    response = await client.get(f"/api/v1/items/{item_id}")
    assert response.status_code == 200
    assert response.json()["id"] == item_id


@pytest.mark.asyncio
async def test_get_item_not_found(client: AsyncClient) -> None:
    response = await client.get("/api/v1/items/99999")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_update_item(client: AsyncClient) -> None:
    create_resp = await client.post("/api/v1/items", json={"title": "Original"})
    item_id = create_resp.json()["id"]

    response = await client.put(f"/api/v1/items/{item_id}", json={"title": "Updated"})
    assert response.status_code == 200
    assert response.json()["title"] == "Updated"


@pytest.mark.asyncio
async def test_delete_item(client: AsyncClient) -> None:
    create_resp = await client.post("/api/v1/items", json={"title": "To delete"})
    item_id = create_resp.json()["id"]

    delete_resp = await client.delete(f"/api/v1/items/{item_id}")
    assert delete_resp.status_code == 204

    get_resp = await client.get(f"/api/v1/items/{item_id}")
    assert get_resp.status_code == 404


@pytest.mark.asyncio
async def test_create_item_invalid_payload(client: AsyncClient) -> None:
    # Title is required
    response = await client.post("/api/v1/items", json={})
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_list_items_pagination(client: AsyncClient) -> None:
    for i in range(5):
        await client.post("/api/v1/items", json={"title": f"Item {i}"})

    response = await client.get("/api/v1/items?skip=0&limit=3")
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) == 3
    assert data["total"] == 5
