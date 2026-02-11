"""FastAPI web API for the Prompt Plugin."""

from __future__ import annotations

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from typing import Optional

from prompt_plugin.engine import PromptEngine
from prompt_plugin.history import HistoryManager
from prompt_plugin.models import (
    EnhancedPrompt,
    HistoryEntry,
    PromptRequest,
    TaskCategory,
    TemplateInfo,
)
from prompt_plugin.templates import get_template, list_templates, render_template

# ── App Setup ──────────────────────────────────────────────────────────────────

app = FastAPI(
    title="Prompt Plugin",
    description="AI prompt enhancement API — auto-enhance, template, and manage prompts",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

engine = PromptEngine()
history = engine.history

STATIC_DIR = Path(__file__).parent / "static"


# ── API Routes ─────────────────────────────────────────────────────────────────

@app.post("/api/enhance", response_model=EnhancedPrompt, tags=["Prompts"])
async def enhance(request: PromptRequest):
    """Enhance a raw prompt with auto-detection, tone styling, and context."""
    return engine.process(request)


# ── Templates ──────────────────────────────────────────────────────────────────

@app.get("/api/templates", response_model=list[TemplateInfo], tags=["Templates"])
async def templates(category: Optional[TaskCategory] = None):
    """List available prompt templates, optionally filtered by category."""
    return list_templates(category)


@app.get("/api/templates/{template_id}", response_model=TemplateInfo, tags=["Templates"])
async def template_detail(template_id: str):
    """Get details of a specific template."""
    tmpl = get_template(template_id)
    if not tmpl:
        raise HTTPException(404, f"Template '{template_id}' not found")
    return tmpl


@app.post("/api/templates/{template_id}/render", tags=["Templates"])
async def template_render(template_id: str, variables: dict[str, str]):
    """Render a template with provided variables."""
    try:
        rendered = render_template(template_id, variables)
    except ValueError as exc:
        raise HTTPException(404, str(exc))
    return {"template_id": template_id, "rendered": rendered}


# ── History ────────────────────────────────────────────────────────────────────

@app.get("/api/history", response_model=list[HistoryEntry], tags=["History"])
async def get_history(
    category: Optional[TaskCategory] = None,
    limit: int = Query(20, ge=1, le=100),
    starred: bool = False,
):
    """Get recent prompt history."""
    return history.list(category=category, limit=limit, starred_only=starred)


@app.get("/api/history/search", response_model=list[HistoryEntry], tags=["History"])
async def search_history(q: str = Query(..., min_length=1), limit: int = 10):
    """Search prompt history."""
    return history.search(q, limit=limit)


@app.post("/api/history/{entry_id}/star", response_model=HistoryEntry, tags=["History"])
async def toggle_star(entry_id: int):
    """Toggle starred status of a history entry."""
    entry = history.star(entry_id)
    if not entry:
        raise HTTPException(404, f"History entry {entry_id} not found")
    return entry


@app.delete("/api/history/{entry_id}", tags=["History"])
async def delete_entry(entry_id: int):
    """Delete a history entry."""
    if not history.delete(entry_id):
        raise HTTPException(404, f"History entry {entry_id} not found")
    return {"deleted": entry_id}


@app.delete("/api/history", tags=["History"])
async def clear_history():
    """Clear all history."""
    count = history.clear()
    return {"cleared": count}


# ── Web UI ─────────────────────────────────────────────────────────────────────

@app.get("/", response_class=HTMLResponse, include_in_schema=False)
async def serve_ui():
    """Serve the web UI."""
    index = STATIC_DIR / "index.html"
    if index.exists():
        return HTMLResponse(index.read_text())
    return HTMLResponse("<h1>Prompt Plugin API</h1><p>Visit <a href='/docs'>/docs</a> for API documentation.</p>")
