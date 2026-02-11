# 🔥 Prompt Plugin

AI prompt enhancement toolkit that turns vague prompts into structured, high-quality instructions for better results from ChatGPT, Claude, Gemini, and other AI chatbots.

<img width="1878" height="701" alt="image" src="https://github.com/user-attachments/assets/d31f9ccc-8bb4-42af-b5c3-6a5151626832" />

## The Problem

Most people type quick, unstructured prompts into AI chatbots and get generic, shallow responses. Prompt engineering makes a huge difference in output quality — but writing detailed, well-structured prompts every time is tedious and requires expertise most users don't have.

## The Solution

Prompt Plugin sits between you and any AI chatbot. You type your rough idea, and it automatically:

1. **Detects what you're trying to do** — coding, writing, analysis, debugging, brainstorming, etc.
2. **Adds expert role framing** — e.g. "You are an expert software engineer" for coding tasks
3. **Applies tone styling** — matches your chosen tone (professional, casual, technical, etc.)
4. **Boosts specificity** — if your prompt is too vague, it adds detail and example requests
5. **Injects structure** — asks the AI to organize its response (sections, bullet points, code + explanation)
6. **Adds quality guardrails** — instructs the AI to prioritize accuracy, flag uncertainty, and use examples

The result is a prompt that consistently produces better, more useful AI responses — without you having to think about prompt engineering.

## What It Does

```
❌  "sort a list in python"

✅  "You are an expert software engineer. Write Python code that sorts a list.
    Follow best practices, include comments, handle edge cases, and provide
    example usage."
```

```
❌  "explain docker"

✅  "You are a patient teacher who explains complex topics clearly.
    Explain the concept of Docker. Include a simple overview, a real-world
    analogy, key terminology, a practical example, and common misconceptions.
    Be warm, approachable, and encouraging."
```

## Who It's For

- **Developers** who use AI for coding help and want better code output
- **Writers & marketers** who need AI-generated content that actually sounds good
- **Students & researchers** who want clear, structured explanations
- **Teams** who want a shared set of prompt templates and consistent AI interactions
- **Anyone** who uses ChatGPT, Claude, or Gemini daily and wants better results with less effort

## How It Works

Prompt Plugin uses a rule-based enhancement pipeline (no API keys needed, no external AI calls). Everything runs locally:

- **Category Detection** — keyword analysis across 9 task categories to classify your prompt
- **Template Engine** — 12 pre-built templates with variable substitution for common tasks
- **Enhancement Pipeline** — 6-stage processing chain: role framing → tone → specificity → structure → context → guardrails
- **History Manager** — local JSON-backed storage for saving, searching, and starring past prompts

Available as four interfaces:
- **Web UI** — browser-based dashboard with live enhancement
- **REST API** — FastAPI with Swagger docs, integrate into any app
- **CLI** — terminal tool with rich formatting, clipboard copy
- **Python library** — import and use directly in your code

## Features

- **Auto-Enhance** — rewrites vague prompts with role framing, specificity boosts, and guardrails
- **12 Templates** — coding, writing, analysis, brainstorming, debugging, summarization, translation, explanation
- **6 Tones** — professional, casual, technical, creative, academic, friendly
- **Context Injection** — append extra context and system instructions
- **Prompt History** — save, search, star, and reuse past prompts
- **Auto Category Detection** — detects coding, writing, analysis, etc. from prompt text

## Install

```bash
pip install -e ".[dev]"
```

## Usage

**CLI:**
```bash
prompt-plugin enhance "write a python function to sort a list"
prompt-plugin enhance "explain docker" --tone friendly --context "audience is beginners"
prompt-plugin templates
prompt-plugin history
```

**Web UI + API:**
```bash
prompt-plugin serve
# Web UI → http://127.0.0.1:8000
# API docs → http://127.0.0.1:8000/docs
```

**Python:**
```python
from prompt_plugin.engine import PromptEngine
from prompt_plugin.models import PromptRequest, Tone

engine = PromptEngine()
result = engine.process(PromptRequest(
    raw_prompt="write a python function to sort a list",
    tone=Tone.technical,
))
print(result.enhanced)
```

## Deploy

**Render (free):** Push to GitHub → [render.com](https://render.com) → New Web Service → connect repo → Deploy.

**Docker:**
```bash
docker build -t prompt-plugin .
docker run -p 8000:8000 prompt-plugin
```

## Tests

```bash
pytest -v
```

## License

MIT
