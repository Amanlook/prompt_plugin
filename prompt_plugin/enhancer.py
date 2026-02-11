"""Auto-enhance engine — rewrites vague prompts into structured, effective ones."""

from __future__ import annotations

import re
from prompt_plugin.models import TaskCategory, Tone


# ── Category Detection ─────────────────────────────────────────────────────────

_CATEGORY_KEYWORDS: dict[TaskCategory, list[str]] = {
    TaskCategory.coding: [
        "code", "function", "class", "script", "program", "implement", "api",
        "bug", "error", "syntax", "compile", "algorithm", "database", "sql",
        "python", "javascript", "typescript", "java", "rust", "html", "css",
        "react", "django", "flask", "fastapi", "node", "docker", "git",
    ],
    TaskCategory.debugging: [
        "debug", "fix", "error", "traceback", "exception", "crash", "broken",
        "not working", "fails", "issue", "stack trace", "segfault",
    ],
    TaskCategory.writing: [
        "write", "draft", "compose", "essay", "article", "blog", "email",
        "letter", "copy", "content", "narrative", "story", "report",
    ],
    TaskCategory.analysis: [
        "analyze", "analyse", "compare", "evaluate", "assess", "review",
        "pros and cons", "tradeoff", "benchmark", "metrics", "data",
    ],
    TaskCategory.brainstorming: [
        "brainstorm", "ideas", "suggest", "creative", "innovate", "think of",
        "come up with", "generate ideas", "possibilities",
    ],
    TaskCategory.summarization: [
        "summarize", "summarise", "summary", "tldr", "tl;dr", "key points",
        "brief", "condense", "shorten", "recap",
    ],
    TaskCategory.translation: [
        "translate", "translation", "convert to", "in spanish", "in french",
        "in german", "in japanese", "in chinese", "in hindi", "localize",
    ],
    TaskCategory.explanation: [
        "explain", "what is", "how does", "how do", "why does", "teach me",
        "eli5", "definition", "meaning of", "concept of", "understand",
    ],
}


def detect_category(text: str) -> TaskCategory:
    """Detect the most likely task category from the prompt text."""
    lower = text.lower()
    scores: dict[TaskCategory, int] = {cat: 0 for cat in TaskCategory}

    for category, keywords in _CATEGORY_KEYWORDS.items():
        for kw in keywords:
            if kw in lower:
                scores[category] += 1

    # Debugging is more specific than coding — prioritize it when both match
    if scores[TaskCategory.debugging] > 0 and scores[TaskCategory.coding] > 0:
        if scores[TaskCategory.debugging] >= scores[TaskCategory.coding]:
            return TaskCategory.debugging

    best = max(scores, key=scores.get)  # type: ignore[arg-type]
    return best if scores[best] > 0 else TaskCategory.general


# ── Tone Mapping ───────────────────────────────────────────────────────────────

_TONE_INSTRUCTIONS: dict[Tone, str] = {
    Tone.professional: "Use a professional, clear, and business-appropriate tone.",
    Tone.casual: "Use a relaxed, conversational tone — like chatting with a friend.",
    Tone.technical: "Use precise technical language with proper terminology.",
    Tone.creative: "Be creative, expressive, and imaginative in your response.",
    Tone.academic: "Use formal academic language with proper citations style.",
    Tone.friendly: "Be warm, approachable, and encouraging in your response.",
}


def get_tone_instruction(tone: Tone) -> str:
    return _TONE_INSTRUCTIONS.get(tone, _TONE_INSTRUCTIONS[Tone.professional])


# ── Enhancement Techniques ─────────────────────────────────────────────────────

def _add_specificity(prompt: str, original_word_count: int = 0) -> tuple[str, bool]:
    """If the original prompt is too short or vague, request specific output."""
    wc = original_word_count if original_word_count > 0 else len(prompt.split())
    if wc < 8:
        return (
            prompt + "\n\nPlease be specific and detailed in your response. "
            "Include concrete examples where relevant."
        ), True
    return prompt, False


def _add_structure_request(prompt: str, category: TaskCategory) -> tuple[str, bool]:
    """Ask the AI to structure its response."""
    structure_hints = {
        TaskCategory.coding: "\n\nStructure your response with: explanation, code, and usage example.",
        TaskCategory.analysis: "\n\nOrganize your analysis with clear sections, bullet points, and a conclusion.",
        TaskCategory.writing: "\n\nUse proper headings, paragraphs, and a logical flow.",
        TaskCategory.explanation: "\n\nStart with a simple overview, then progressively add detail.",
        TaskCategory.debugging: "\n\nStructure: identify the bug → explain the cause → provide the fix → suggest prevention.",
        TaskCategory.brainstorming: "\n\nPresent ideas in a numbered list with brief descriptions.",
        TaskCategory.summarization: "\n\nProvide an executive summary, then key bullet points.",
    }
    hint = structure_hints.get(category)
    if hint:
        return prompt + hint, True
    return prompt, False


def _add_role_framing(prompt: str, category: TaskCategory) -> tuple[str, bool]:
    """Prepend a role/persona for better results."""
    roles = {
        TaskCategory.coding: "You are an expert software engineer with deep knowledge of best practices.",
        TaskCategory.debugging: "You are a senior developer skilled at diagnosing and fixing complex bugs.",
        TaskCategory.writing: "You are a skilled writer who crafts engaging, well-structured content.",
        TaskCategory.analysis: "You are a data analyst who provides clear, evidence-based insights.",
        TaskCategory.brainstorming: "You are a creative strategist who generates innovative solutions.",
        TaskCategory.explanation: "You are a patient teacher who explains complex topics clearly.",
        TaskCategory.summarization: "You are an editor who distills information to its essential points.",
        TaskCategory.translation: "You are a professional translator who preserves meaning and nuance.",
        TaskCategory.general: "You are a helpful, knowledgeable assistant.",
    }
    role = roles.get(category, roles[TaskCategory.general])
    return f"{role}\n\n{prompt}", True


def _add_quality_guardrails(prompt: str) -> tuple[str, bool]:
    """Add instructions to improve output quality."""
    guardrails = (
        "\n\nImportant guidelines:\n"
        "- If you're unsure about something, say so rather than guessing\n"
        "- Prioritize accuracy over completeness\n"
        "- Use concrete examples to illustrate points"
    )
    return prompt + guardrails, True


# ── Main Enhancer ──────────────────────────────────────────────────────────────

def enhance_prompt(
    raw_prompt: str,
    tone: Tone = Tone.professional,
    category: TaskCategory | None = None,
    extra_context: str | None = None,
) -> tuple[str, TaskCategory, list[str]]:
    """
    Enhance a raw user prompt. Returns (enhanced_text, detected_category, techniques_applied).
    """
    detected = category or detect_category(raw_prompt)
    techniques: list[str] = []
    prompt = raw_prompt.strip()

    # 1. Role framing
    prompt, applied = _add_role_framing(prompt, detected)
    if applied:
        techniques.append("role_framing")

    # 2. Tone instruction
    tone_instr = get_tone_instruction(tone)
    prompt += f"\n\n{tone_instr}"
    techniques.append("tone_styling")

    # 3. Specificity boost
    prompt, applied = _add_specificity(prompt, original_word_count=len(raw_prompt.split()))
    if applied:
        techniques.append("specificity_boost")

    # 4. Structure request
    prompt, applied = _add_structure_request(prompt, detected)
    if applied:
        techniques.append("structure_guidance")

    # 5. Context injection
    if extra_context:
        prompt += f"\n\nAdditional context:\n{extra_context}"
        techniques.append("context_injection")

    # 6. Quality guardrails
    prompt, applied = _add_quality_guardrails(prompt)
    if applied:
        techniques.append("quality_guardrails")

    return prompt, detected, techniques
