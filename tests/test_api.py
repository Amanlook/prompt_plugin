"""Tests for the FastAPI endpoints."""

import pytest
from httpx import AsyncClient, ASGITransport
from prompt_plugin.api import app


@pytest.fixture
def client():
    transport = ASGITransport(app=app)
    return AsyncClient(transport=transport, base_url="http://test")


@pytest.mark.asyncio
async def test_enhance_endpoint(client):
    async with client as c:
        res = await c.post("/api/enhance", json={
            "raw_prompt": "explain recursion",
            "tone": "friendly",
        })
    assert res.status_code == 200
    data = res.json()
    assert "enhanced" in data
    assert data["category"] == "explanation"


@pytest.mark.asyncio
async def test_list_templates(client):
    async with client as c:
        res = await c.get("/api/templates")
    assert res.status_code == 200
    templates = res.json()
    assert len(templates) > 0


@pytest.mark.asyncio
async def test_template_detail(client):
    async with client as c:
        res = await c.get("/api/templates/code-write")
    assert res.status_code == 200
    assert res.json()["id"] == "code-write"


@pytest.mark.asyncio
async def test_template_not_found(client):
    async with client as c:
        res = await c.get("/api/templates/nonexistent")
    assert res.status_code == 404


@pytest.mark.asyncio
async def test_render_template(client):
    async with client as c:
        res = await c.post("/api/templates/code-write/render", json={
            "language": "Go",
            "task_description": "HTTP server",
        })
    assert res.status_code == 200
    assert "Go" in res.json()["rendered"]


@pytest.mark.asyncio
async def test_root_serves_html(client):
    async with client as c:
        res = await c.get("/")
    assert res.status_code == 200
    assert "Prompt Plugin" in res.text
