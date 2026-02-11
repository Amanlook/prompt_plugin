"""Tests for the prompt plugin core engine."""

from prompt_plugin.enhancer import detect_category, enhance_prompt
from prompt_plugin.engine import PromptEngine
from prompt_plugin.history import HistoryManager
from prompt_plugin.models import PromptRequest, TaskCategory, Tone
from prompt_plugin.templates import get_template, list_templates, render_template
from pathlib import Path
import tempfile


# ── Category Detection ─────────────────────────────────────────────────────────

def test_detect_coding():
    assert detect_category("write a python function to sort a list") == TaskCategory.coding


def test_detect_debugging():
    assert detect_category("fix this error: TypeError in my code") == TaskCategory.debugging


def test_detect_writing():
    assert detect_category("write an article about AI trends") == TaskCategory.writing


def test_detect_explanation():
    assert detect_category("explain how neural networks work") == TaskCategory.explanation


def test_detect_general():
    assert detect_category("hello world") == TaskCategory.general


# ── Enhancer ───────────────────────────────────────────────────────────────────

def test_enhance_adds_role():
    enhanced, cat, techs = enhance_prompt("write python code for sorting")
    assert "expert software engineer" in enhanced.lower() or "role_framing" in techs


def test_enhance_applies_tone():
    enhanced, _, techs = enhance_prompt("help me", tone=Tone.casual)
    assert "tone_styling" in techs
    assert "conversational" in enhanced.lower() or "casual" in enhanced.lower() or "relaxed" in enhanced.lower()


def test_enhance_injects_context():
    enhanced, _, techs = enhance_prompt("sort a list", extra_context="Using Python 3.12")
    assert "Python 3.12" in enhanced
    assert "context_injection" in techs


def test_enhance_short_prompt_gets_specificity():
    enhanced, _, techs = enhance_prompt("help")
    assert "specificity_boost" in techs


# ── Templates ──────────────────────────────────────────────────────────────────

def test_list_templates():
    templates = list_templates()
    assert len(templates) > 0


def test_list_templates_filter():
    coding = list_templates(TaskCategory.coding)
    assert all(t.category == TaskCategory.coding for t in coding)


def test_get_template():
    tmpl = get_template("code-write")
    assert tmpl is not None
    assert tmpl.name == "Write Code"


def test_render_template():
    rendered = render_template("code-write", {
        "language": "Python",
        "task_description": "sort a list of numbers"
    })
    assert "Python" in rendered
    assert "sort a list of numbers" in rendered


# ── History ────────────────────────────────────────────────────────────────────

def test_history_crud():
    with tempfile.TemporaryDirectory() as tmpdir:
        hm = HistoryManager(path=Path(tmpdir) / "test_history.json")

        entry = hm.add("raw", "enhanced", TaskCategory.coding, Tone.professional)
        assert entry.id == 1
        assert hm.count == 1

        # List
        items = hm.list()
        assert len(items) == 1

        # Star
        starred = hm.star(1)
        assert starred.starred is True

        # Search
        results = hm.search("raw")
        assert len(results) == 1

        # Delete
        assert hm.delete(1) is True
        assert hm.count == 0


def test_history_persistence():
    with tempfile.TemporaryDirectory() as tmpdir:
        path = Path(tmpdir) / "persist.json"
        hm1 = HistoryManager(path=path)
        hm1.add("test", "test enhanced", TaskCategory.general, Tone.casual)

        hm2 = HistoryManager(path=path)
        assert hm2.count == 1


# ── Engine Integration ─────────────────────────────────────────────────────────

def test_engine_process():
    with tempfile.TemporaryDirectory() as tmpdir:
        hm = HistoryManager(path=Path(tmpdir) / "engine_hist.json")
        engine = PromptEngine(history=hm)

        result = engine.process(PromptRequest(
            raw_prompt="write a python function to reverse a string",
            tone=Tone.technical,
        ))

        assert result.category == TaskCategory.coding
        assert "reverse" in result.enhanced.lower()
        assert len(result.techniques_applied) > 0
        assert hm.count == 1


def test_engine_with_template():
    with tempfile.TemporaryDirectory() as tmpdir:
        hm = HistoryManager(path=Path(tmpdir) / "tmpl_hist.json")
        engine = PromptEngine(history=hm)

        result = engine.process(PromptRequest(
            raw_prompt='{"language": "Rust", "task_description": "read a file"}',
            template_id="code-write",
            tone=Tone.technical,
        ))

        assert "Rust" in result.enhanced
        assert "read a file" in result.enhanced
