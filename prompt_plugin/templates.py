"""Built-in prompt templates for common AI tasks."""

from __future__ import annotations

from prompt_plugin.models import TaskCategory, TemplateInfo

# ── Template Registry ──────────────────────────────────────────────────────────

TEMPLATES: dict[str, TemplateInfo] = {}


def _register(t: TemplateInfo) -> None:
    TEMPLATES[t.id] = t


# ── Coding Templates ──────────────────────────────────────────────────────────

_register(TemplateInfo(
    id="code-write",
    name="Write Code",
    category=TaskCategory.coding,
    description="Generate clean, well-documented code for a given task",
    template=(
        "Write {language} code that accomplishes the following:\n\n"
        "{task_description}\n\n"
        "Requirements:\n"
        "- Follow best practices and idiomatic patterns for {language}\n"
        "- Include clear comments explaining the logic\n"
        "- Handle edge cases and errors gracefully\n"
        "- Provide example usage"
    ),
    variables=["language", "task_description"],
))

_register(TemplateInfo(
    id="code-review",
    name="Code Review",
    category=TaskCategory.coding,
    description="Get a thorough code review with actionable suggestions",
    template=(
        "Perform a detailed code review of the following code:\n\n"
        "```{language}\n{code}\n```\n\n"
        "Evaluate for:\n"
        "1. Correctness and potential bugs\n"
        "2. Performance and efficiency\n"
        "3. Readability and maintainability\n"
        "4. Security concerns\n"
        "5. Adherence to {language} best practices\n\n"
        "Provide specific, actionable suggestions with code examples."
    ),
    variables=["language", "code"],
))

_register(TemplateInfo(
    id="code-debug",
    name="Debug Code",
    category=TaskCategory.debugging,
    description="Systematically debug code issues",
    template=(
        "I have the following {language} code that is producing an error:\n\n"
        "```{language}\n{code}\n```\n\n"
        "Error message: {error_message}\n\n"
        "Please:\n"
        "1. Identify the root cause of the error\n"
        "2. Explain why the error occurs\n"
        "3. Provide the corrected code\n"
        "4. Suggest how to prevent similar issues"
    ),
    variables=["language", "code", "error_message"],
))

# ── Writing Templates ─────────────────────────────────────────────────────────

_register(TemplateInfo(
    id="write-article",
    name="Write Article",
    category=TaskCategory.writing,
    description="Create a well-structured article on any topic",
    template=(
        "Write a comprehensive article about: {topic}\n\n"
        "Target audience: {audience}\n"
        "Desired length: {length}\n\n"
        "Structure the article with:\n"
        "- An engaging introduction that hooks the reader\n"
        "- Well-organized sections with clear headings\n"
        "- Supporting evidence, examples, or data points\n"
        "- A compelling conclusion with key takeaways\n\n"
        "Tone: {tone}"
    ),
    variables=["topic", "audience", "length", "tone"],
))

_register(TemplateInfo(
    id="write-email",
    name="Compose Email",
    category=TaskCategory.writing,
    description="Draft a professional or casual email",
    template=(
        "Draft an email with the following details:\n\n"
        "Purpose: {purpose}\n"
        "Recipient: {recipient}\n"
        "Key points to cover:\n{key_points}\n\n"
        "Tone: {tone}\n"
        "Keep it concise and action-oriented."
    ),
    variables=["purpose", "recipient", "key_points", "tone"],
))

# ── Analysis Templates ────────────────────────────────────────────────────────

_register(TemplateInfo(
    id="analyze-data",
    name="Analyze Data",
    category=TaskCategory.analysis,
    description="Get structured analysis of data or information",
    template=(
        "Analyze the following data/information:\n\n"
        "{data}\n\n"
        "Please provide:\n"
        "1. Key findings and patterns\n"
        "2. Notable outliers or anomalies\n"
        "3. Trends and correlations\n"
        "4. Actionable insights and recommendations\n"
        "5. Limitations of this analysis\n\n"
        "Focus area: {focus_area}"
    ),
    variables=["data", "focus_area"],
))

_register(TemplateInfo(
    id="compare-options",
    name="Compare Options",
    category=TaskCategory.analysis,
    description="Get a structured comparison of multiple options",
    template=(
        "Compare the following options:\n\n"
        "{options}\n\n"
        "Evaluation criteria: {criteria}\n\n"
        "For each option provide:\n"
        "- Pros and cons\n"
        "- Best use cases\n"
        "- Cost/effort considerations\n"
        "- Final recommendation with justification"
    ),
    variables=["options", "criteria"],
))

# ── Brainstorming Templates ──────────────────────────────────────────────────

_register(TemplateInfo(
    id="brainstorm-ideas",
    name="Brainstorm Ideas",
    category=TaskCategory.brainstorming,
    description="Generate creative ideas for a topic or problem",
    template=(
        "Generate creative and diverse ideas for:\n\n"
        "{topic}\n\n"
        "Constraints: {constraints}\n\n"
        "Please provide:\n"
        "- At least 10 unique ideas ranging from practical to innovative\n"
        "- A brief description of each idea\n"
        "- Why each idea could work\n"
        "- Quick feasibility rating (Easy / Medium / Hard)"
    ),
    variables=["topic", "constraints"],
))

# ── Summarization Templates ──────────────────────────────────────────────────

_register(TemplateInfo(
    id="summarize-text",
    name="Summarize Text",
    category=TaskCategory.summarization,
    description="Create concise summaries of long content",
    template=(
        "Summarize the following content:\n\n"
        "{content}\n\n"
        "Provide:\n"
        "1. A one-paragraph executive summary\n"
        "2. Key bullet points (5-7 items)\n"
        "3. Important details that shouldn't be missed\n"
        "4. Action items or next steps (if applicable)"
    ),
    variables=["content"],
))

# ── Explanation Templates ─────────────────────────────────────────────────────

_register(TemplateInfo(
    id="explain-concept",
    name="Explain Concept",
    category=TaskCategory.explanation,
    description="Get a clear explanation of any concept",
    template=(
        "Explain the concept of: {concept}\n\n"
        "Target knowledge level: {level}\n\n"
        "Please include:\n"
        "- A simple, intuitive explanation\n"
        "- A real-world analogy\n"
        "- Key terminology defined\n"
        "- A practical example\n"
        "- Common misconceptions to avoid\n"
        "- Resources for deeper learning"
    ),
    variables=["concept", "level"],
))

_register(TemplateInfo(
    id="eli5",
    name="Explain Like I'm 5",
    category=TaskCategory.explanation,
    description="Super-simple explanation for complex topics",
    template=(
        "Explain {concept} in the simplest possible terms, as if I'm 5 years old.\n\n"
        "Use:\n"
        "- Everyday analogies and examples\n"
        "- Short, simple sentences\n"
        "- No jargon or technical terms\n"
        "- A fun, engaging tone"
    ),
    variables=["concept"],
))

# ── Translation Template ──────────────────────────────────────────────────────

_register(TemplateInfo(
    id="translate-text",
    name="Translate Text",
    category=TaskCategory.translation,
    description="Translate text while preserving meaning and nuance",
    template=(
        "Translate the following text from {source_language} to {target_language}:\n\n"
        "{text}\n\n"
        "Requirements:\n"
        "- Preserve the original meaning, tone, and nuance\n"
        "- Use natural phrasing in the target language\n"
        "- Note any cultural context that affects the translation\n"
        "- Flag any ambiguous phrases with alternative translations"
    ),
    variables=["source_language", "target_language", "text"],
))


# ── Public API ────────────────────────────────────────────────────────────────

def get_template(template_id: str) -> TemplateInfo | None:
    """Return a template by ID."""
    return TEMPLATES.get(template_id)


def list_templates(category: TaskCategory | None = None) -> list[TemplateInfo]:
    """List all templates, optionally filtered by category."""
    templates = list(TEMPLATES.values())
    if category:
        templates = [t for t in templates if t.category == category]
    return templates


def render_template(template_id: str, variables: dict[str, str]) -> str:
    """Fill in a template with the given variables. Missing vars become placeholders."""
    tmpl = TEMPLATES.get(template_id)
    if not tmpl:
        raise ValueError(f"Unknown template: {template_id}")

    result = tmpl.template
    for var in tmpl.variables:
        placeholder = "{" + var + "}"
        value = variables.get(var, f"[{var}]")
        result = result.replace(placeholder, value)
    return result
