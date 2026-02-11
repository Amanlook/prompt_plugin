"""CLI interface for the Prompt Plugin (powered by Typer + Rich)."""

from __future__ import annotations

import json
from typing import Optional

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from prompt_plugin.engine import PromptEngine
from prompt_plugin.models import PromptRequest, TaskCategory, Tone
from prompt_plugin.templates import list_templates, render_template

app = typer.Typer(
    name="prompt-plugin",
    help="AI Prompt Plugin — enhance, template, and manage prompts from the terminal.",
    rich_markup_mode="rich",
)
console = Console()
engine = PromptEngine()


# ── Enhance Command ────────────────────────────────────────────────────────────

@app.command()
def enhance(
    prompt: str = typer.Argument(..., help="The raw prompt to enhance"),
    tone: Tone = typer.Option(Tone.professional, "--tone", "-t", help="Desired output tone"),
    category: Optional[TaskCategory] = typer.Option(None, "--category", "-c", help="Force a task category"),
    context: Optional[str] = typer.Option(None, "--context", help="Extra context to inject"),
    template: Optional[str] = typer.Option(None, "--template", help="Template ID to use"),
    no_enhance: bool = typer.Option(False, "--raw", help="Skip auto-enhancement"),
    copy: bool = typer.Option(False, "--copy", help="Copy result to clipboard (macOS)"),
):
    """Enhance a prompt for better AI chatbot results."""
    request = PromptRequest(
        raw_prompt=prompt,
        tone=tone,
        category=category,
        context=context,
        auto_enhance=not no_enhance,
        template_id=template,
    )
    result = engine.process(request)

    # Display
    console.print()
    console.print(Panel(
        result.enhanced,
        title=f"[bold green]Enhanced Prompt[/] — {result.category.value} / {result.tone.value}",
        subtitle=f"Techniques: {', '.join(result.techniques_applied) or 'none'}",
        border_style="green",
        padding=(1, 2),
    ))

    if copy:
        try:
            import subprocess
            subprocess.run(["pbcopy"], input=result.enhanced.encode(), check=True)
            console.print("[dim]Copied to clipboard.[/dim]")
        except Exception:
            console.print("[yellow]Could not copy to clipboard.[/yellow]")


# ── Templates Commands ─────────────────────────────────────────────────────────

@app.command(name="templates")
def list_tmpl(
    category: Optional[TaskCategory] = typer.Option(None, "--category", "-c"),
):
    """List available prompt templates."""
    templates = list_templates(category)
    table = Table(title="Prompt Templates", show_lines=True)
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("Name", style="bold")
    table.add_column("Category", style="magenta")
    table.add_column("Description")
    table.add_column("Variables", style="dim")

    for t in templates:
        table.add_row(t.id, t.name, t.category.value, t.description, ", ".join(t.variables))

    console.print(table)


@app.command(name="render")
def render_tmpl(
    template_id: str = typer.Argument(..., help="Template ID"),
    variables: str = typer.Argument(..., help='Variables as JSON, e.g. \'{"language": "Python", "task_description": "sort a list"}\''),
):
    """Render a prompt template with given variables."""
    try:
        vars_dict = json.loads(variables)
    except json.JSONDecodeError:
        console.print("[red]Invalid JSON for variables.[/red]")
        raise typer.Exit(1)

    try:
        rendered = render_template(template_id, vars_dict)
    except ValueError as e:
        console.print(f"[red]{e}[/red]")
        raise typer.Exit(1)

    console.print(Panel(rendered, title=f"[bold]Template: {template_id}[/]", border_style="blue"))


# ── History Commands ───────────────────────────────────────────────────────────

@app.command(name="history")
def show_history(
    limit: int = typer.Option(10, "--limit", "-n"),
    category: Optional[TaskCategory] = typer.Option(None, "--category", "-c"),
    starred: bool = typer.Option(False, "--starred", "-s"),
    search: Optional[str] = typer.Option(None, "--search", "-q"),
):
    """Show prompt history."""
    history = engine.history

    if search:
        entries = history.search(search, limit=limit)
    else:
        entries = history.list(category=category, limit=limit, starred_only=starred)

    if not entries:
        console.print("[dim]No history entries found.[/dim]")
        return

    table = Table(title="Prompt History", show_lines=True)
    table.add_column("ID", style="cyan", width=5)
    table.add_column("Star", width=4)
    table.add_column("Category", style="magenta", width=14)
    table.add_column("Original", max_width=40)
    table.add_column("Tone", width=12)
    table.add_column("Time", style="dim", width=19)

    for e in entries:
        star = "⭐" if e.starred else ""
        orig = e.original[:80] + "…" if len(e.original) > 80 else e.original
        table.add_row(
            str(e.id), star, e.category.value, orig,
            e.tone.value, e.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
        )

    console.print(table)


@app.command(name="clear-history")
def clear_hist():
    """Clear all prompt history."""
    count = engine.history.clear()
    console.print(f"[green]Cleared {count} history entries.[/green]")


# ── Server Command ─────────────────────────────────────────────────────────────

@app.command(name="serve")
def serve(
    host: str = typer.Option("127.0.0.1", "--host"),
    port: int = typer.Option(8000, "--port", "-p"),
    reload: bool = typer.Option(False, "--reload"),
):
    """Start the Prompt Plugin web API server."""
    import uvicorn
    console.print(f"[bold green]Starting Prompt Plugin server at http://{host}:{port}[/bold green]")
    console.print("[dim]API docs at /docs  •  Web UI at /[/dim]")
    uvicorn.run("prompt_plugin.api:app", host=host, port=port, reload=reload)


if __name__ == "__main__":
    app()
