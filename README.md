# 🔥 Prompt Plugin

> **Stop writing bad prompts.** Prompt Plugin is an open-source AI prompt enhancement toolkit that automatically transforms your vague, incomplete prompts into structured, high-quality instructions — so ChatGPT, Claude, Gemini, and other AI chatbots give you dramatically better results.

Whether you're coding, writing, analyzing data, or brainstorming — just type your rough idea and Prompt Plugin handles the rest: it detects the task type, applies expert role framing, injects structure and context, and polishes tone. Available as a **Web UI**, **REST API**, **CLI tool**, and **Python library**.

---

## Features

| Feature | Description |
|---------|-------------|
| **Auto-Enhance** | Rewrites vague prompts into structured, effective ones using role framing, specificity boosts, and quality guardrails |
| **12 Prompt Templates** | Pre-built templates for coding, writing, analysis, brainstorming, debugging, summarization, translation, and more |
| **Tone/Style Selector** | Choose from 6 tones: Professional, Casual, Technical, Creative, Academic, Friendly |
| **Context Injection** | Automatically adds relevant context and system instructions to your prompts |
| **Prompt History** | Save, search, star, and reuse past prompts with persistent local storage |
| **Auto Category Detection** | Detects task type (coding, writing, analysis, etc.) from your prompt text |

## Quick Start

### Install

```bash
cd prompt_plugin
pip install -e ".[dev]"
```

### CLI Usage

```bash
# Enhance a prompt
prompt-plugin enhance "write a python function to sort a list"

# With tone and context
prompt-plugin enhance "explain docker" --tone friendly --context "audience is beginners"

# Copy result to clipboard (macOS)
prompt-plugin enhance "compare React vs Vue" --copy

# List templates
prompt-plugin templates

# Render a template
prompt-plugin render code-write '{"language": "Python", "task_description": "binary search"}'

# View history
prompt-plugin history
prompt-plugin history --starred
prompt-plugin history --search "python"

# Start the web server
prompt-plugin serve
```

### Web API & UI

```bash
# Start the server
prompt-plugin serve

# Or directly with uvicorn
uvicorn prompt_plugin.api:app --reload
```

Then open:
- **Web UI**: http://127.0.0.1:8000
- **API Docs (Swagger)**: http://127.0.0.1:8000/docs

### API Examples

```bash
# Enhance a prompt
curl -X POST http://127.0.0.1:8000/api/enhance \
  -H "Content-Type: application/json" \
  -d '{"raw_prompt": "fix my code", "tone": "technical"}'

# List templates
curl http://127.0.0.1:8000/api/templates

# Render a template
curl -X POST http://127.0.0.1:8000/api/templates/code-write/render \
  -H "Content-Type: application/json" \
  -d '{"language": "Go", "task_description": "HTTP server"}'
```

### Python Library

```python
from prompt_plugin.engine import PromptEngine
from prompt_plugin.models import PromptRequest, Tone

engine = PromptEngine()
result = engine.process(PromptRequest(
    raw_prompt="write a python function to sort a list",
    tone=Tone.technical,
    context="Using Python 3.12",
))

print(result.enhanced)       # The improved prompt
print(result.category)       # TaskCategory.coding
print(result.techniques_applied)  # ['role_framing', 'tone_styling', ...]
```

## How Enhancement Works

The engine applies these techniques in order:

1. **Role Framing** — Prepends an expert persona matching the detected task category
2. **Tone Styling** — Adds tone instructions (professional, casual, etc.)
3. **Specificity Boost** — If the prompt is too short/vague, adds detail requests
4. **Structure Guidance** — Requests organized output format based on category
5. **Context Injection** — Appends any extra context the user provides
6. **Quality Guardrails** — Adds instructions for accuracy and examples

## Templates

| Template | Category | Variables |
|----------|----------|-----------|
| Write Code | coding | `language`, `task_description` |
| Code Review | coding | `language`, `code` |
| Debug Code | debugging | `language`, `code`, `error_message` |
| Write Article | writing | `topic`, `audience`, `length`, `tone` |
| Compose Email | writing | `purpose`, `recipient`, `key_points`, `tone` |
| Analyze Data | analysis | `data`, `focus_area` |
| Compare Options | analysis | `options`, `criteria` |
| Brainstorm Ideas | brainstorming | `topic`, `constraints` |
| Summarize Text | summarization | `content` |
| Explain Concept | explanation | `concept`, `level` |
| ELI5 | explanation | `concept` |
| Translate Text | translation | `source_language`, `target_language`, `text` |

## Running Tests

```bash
pip install -e ".[dev]"
pytest -v
```

## Project Structure

```
prompt_plugin/
├── prompt_plugin/
│   ├── __init__.py         # Package metadata
│   ├── models.py           # Pydantic data models
│   ├── templates.py        # 12 built-in prompt templates
│   ├── enhancer.py         # Auto-enhance engine + category detection
│   ├── history.py          # Persistent prompt history manager
│   ├── engine.py           # Main orchestrator
│   ├── api.py              # FastAPI web API
│   ├── cli.py              # Typer CLI interface
│   └── static/
│       └── index.html      # Web UI (single-page app)
├── tests/
│   ├── test_core.py        # Core engine tests
│   └── test_api.py         # API endpoint tests
├── pyproject.toml           # Project config & dependencies
└── README.md
```

## License

MIT
