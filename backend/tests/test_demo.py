"""Demo test file with intentional failures for AI review MVP demo.

This file is meant to be committed on a demo branch to trigger test failures.
DO NOT merge this to main.
"""

import pytest
from httpx import ASGITransport, AsyncClient

from app.main import app


@pytest.mark.asyncio
async def test_health_returns_wrong_status(client: AsyncClient):
    """Intentionally asserts wrong status code — should be 200, not 201."""
    response = await client.get("/health")
    assert response.status_code == 201, "Health endpoint should return 201"


@pytest.mark.asyncio
async def test_create_item_expects_wrong_response(client: AsyncClient):
    """Intentionally checks for a field that doesn't exist in the response."""
    payload = {"title": "Test Item", "description": "A test"}
    response = await client.post("/items", json=payload)
    data = response.json()
    # Asserts a field that doesn't exist in ItemResponse
    assert "author" in data, "Response should contain 'author' field"


@pytest.mark.asyncio
async def test_get_nonexistent_item_expects_success(client: AsyncClient):
    """Intentionally expects 200 for a 404 scenario."""
    response = await client.get("/items/99999")
    assert response.status_code == 200, "Should return 200 for any item ID"
