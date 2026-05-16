"""Tests for the conversations CRUD API."""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_list_conversations_empty(client: AsyncClient) -> None:
    response = await client.get("/api/v1/conversations")
    assert response.status_code == 200
    data = response.json()
    assert data["conversations"] == []
    assert data["total"] == 0


@pytest.mark.asyncio
async def test_create_conversation(client: AsyncClient) -> None:
    payload = {"title": "Test Chat", "provider": "openai", "model": "gpt-4o"}
    response = await client.post("/api/v1/conversations", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Chat"
    assert data["provider"] == "openai"
    assert "id" in data


@pytest.mark.asyncio
async def test_get_conversation(client: AsyncClient) -> None:
    create_resp = await client.post(
        "/api/v1/conversations",
        json={"title": "My Chat", "provider": "openai", "model": "gpt-4o"},
    )
    conv_id = create_resp.json()["id"]

    response = await client.get(f"/api/v1/conversations/{conv_id}")
    assert response.status_code == 200
    assert response.json()["id"] == conv_id
    assert response.json()["messages"] == []


@pytest.mark.asyncio
async def test_get_conversation_not_found(client: AsyncClient) -> None:
    response = await client.get("/api/v1/conversations/00000000-0000-0000-0000-000000000000")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_delete_conversation(client: AsyncClient) -> None:
    create_resp = await client.post(
        "/api/v1/conversations",
        json={"title": "To Delete", "provider": "openai", "model": "gpt-4o"},
    )
    conv_id = create_resp.json()["id"]

    delete_resp = await client.delete(f"/api/v1/conversations/{conv_id}")
    assert delete_resp.status_code == 204

    get_resp = await client.get(f"/api/v1/conversations/{conv_id}")
    assert get_resp.status_code == 404
