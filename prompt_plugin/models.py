"""Core data models for the prompt plugin."""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


# ── Enums ──────────────────────────────────────────────────────────────────────

class Tone(str, Enum):
    professional = "professional"
    casual = "casual"
    technical = "technical"
    creative = "creative"
    academic = "academic"
    friendly = "friendly"


class TaskCategory(str, Enum):
    coding = "coding"
    writing = "writing"
    analysis = "analysis"
    brainstorming = "brainstorming"
    summarization = "summarization"
    translation = "translation"
    debugging = "debugging"
    explanation = "explanation"
    general = "general"


# ── Request / Response Models ──────────────────────────────────────────────────

class PromptRequest(BaseModel):
    """Incoming raw prompt from the user."""

    raw_prompt: str = Field(..., min_length=1, description="The user's original prompt text")
    tone: Tone = Tone.professional
    category: Optional[TaskCategory] = None
    context: Optional[str] = Field(None, description="Extra context to inject")
    auto_enhance: bool = True
    template_id: Optional[str] = None


class EnhancedPrompt(BaseModel):
    """Result after prompt processing."""

    original: str
    enhanced: str
    category: TaskCategory
    tone: Tone
    techniques_applied: list[str] = []
    timestamp: datetime = Field(default_factory=lambda: datetime.now(tz=__import__('datetime').timezone.utc))


class TemplateInfo(BaseModel):
    """Metadata about a prompt template."""

    id: str
    name: str
    category: TaskCategory
    description: str
    template: str
    variables: list[str] = []


class HistoryEntry(BaseModel):
    """A saved prompt history entry."""

    id: int
    original: str
    enhanced: str
    category: TaskCategory
    tone: Tone
    timestamp: datetime
    starred: bool = False
