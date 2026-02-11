"""Orchestrator — ties together enhancement, templates, context, and history."""

from __future__ import annotations

from prompt_plugin.enhancer import enhance_prompt
from prompt_plugin.history import HistoryManager
from prompt_plugin.models import EnhancedPrompt, PromptRequest, TaskCategory, Tone
from prompt_plugin.templates import render_template


class PromptEngine:
    """Main entry point that processes a PromptRequest end-to-end."""

    def __init__(self, history: HistoryManager | None = None) -> None:
        self.history = history or HistoryManager()

    def process(self, request: PromptRequest) -> EnhancedPrompt:
        """Process a prompt request through the full enhancement pipeline."""

        # Step 1 — if a template is selected, render it first
        base_prompt = request.raw_prompt
        if request.template_id:
            # Treat the raw_prompt as a JSON-like dict of variables, or use as-is
            try:
                import json
                variables = json.loads(base_prompt)
            except (json.JSONDecodeError, TypeError):
                variables = {"task_description": base_prompt, "content": base_prompt}
            base_prompt = render_template(request.template_id, variables)

        # Step 2 — auto-enhance
        if request.auto_enhance:
            enhanced_text, detected_category, techniques = enhance_prompt(
                base_prompt,
                tone=request.tone,
                category=request.category,
                extra_context=request.context,
            )
        else:
            enhanced_text = base_prompt
            detected_category = request.category or TaskCategory.general
            techniques = []

            # Still apply context even without auto-enhance
            if request.context:
                enhanced_text += f"\n\nAdditional context:\n{request.context}"

        result = EnhancedPrompt(
            original=request.raw_prompt,
            enhanced=enhanced_text,
            category=detected_category,
            tone=request.tone,
            techniques_applied=techniques,
        )

        # Step 3 — save to history
        self.history.add(
            original=result.original,
            enhanced=result.enhanced,
            category=result.category,
            tone=result.tone,
        )

        return result
