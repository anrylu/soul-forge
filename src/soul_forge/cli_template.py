import importlib.resources
from pathlib import Path
import shutil

import click
import httpx
from rich.console import Console
from rich.table import Table

console = Console()

CUSTOM_TEMPLATE_DIR = Path.home() / ".soul-forge" / "templates"


def _get_builtin_templates() -> list[Path]:
    agents_dir = importlib.resources.files("soul_forge") / "templates" / "agents"
    return sorted(Path(str(agents_dir)).glob("*.md"))


def _get_custom_templates() -> list[Path]:
    if not CUSTOM_TEMPLATE_DIR.exists():
        return []
    return sorted(CUSTOM_TEMPLATE_DIR.glob("*.md"))


@click.group()
def template():
    """Manage agent templates."""
    pass


@template.command("list")
def template_list():
    """List available templates."""
    table = Table(title="Agent Templates")
    table.add_column("Name", style="cyan")
    table.add_column("Source")

    for f in _get_builtin_templates():
        table.add_row(f.stem, "built-in")

    for f in _get_custom_templates():
        table.add_row(f.stem, "custom")

    console.print(table)


@template.command("add")
@click.argument("source")
def template_add(source: str):
    """Add a template from a URL or file path."""
    CUSTOM_TEMPLATE_DIR.mkdir(parents=True, exist_ok=True)

    if source.startswith("http://") or source.startswith("https://"):
        response = httpx.get(source, follow_redirects=True)
        response.raise_for_status()
        name = source.rstrip("/").split("/")[-1]
        if not name.endswith(".md"):
            name += ".md"
        dest = CUSTOM_TEMPLATE_DIR / name
        dest.write_text(response.text)
    else:
        src = Path(source)
        if not src.exists():
            console.print(f"[red]File not found: {source}[/red]")
            raise SystemExit(1)
        dest = CUSTOM_TEMPLATE_DIR / src.name
        shutil.copy2(src, dest)

    console.print(f"  [green]✅[/green] Template saved to {dest}")


@template.command("update")
def template_update():
    """Re-fetch all URL-sourced custom templates."""
    custom = _get_custom_templates()
    if not custom:
        console.print("No custom templates to update.")
        return
    console.print(f"Found {len(custom)} custom template(s). Manual re-add needed for URL sources.")
