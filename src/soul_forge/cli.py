from pathlib import Path

import click
import yaml
from rich.console import Console
from rich.table import Table

from soul_forge.installer import install_platform, update_platform
from soul_forge.platforms import PLATFORMS, get_platforms_by_ids

console = Console()
CONFIG_FILE = ".soul-forge.yaml"


def _load_config() -> dict | None:
    config_path = Path.cwd() / CONFIG_FILE
    if not config_path.exists():
        return None
    return yaml.safe_load(config_path.read_text())


def _save_config(config: dict) -> None:
    config_path = Path.cwd() / CONFIG_FILE
    config_path.write_text(yaml.dump(config, default_flow_style=False))


@click.group()
def cli():
    """Soul Forge — RPG-style character creation for AI agents."""
    pass


@cli.command()
def init():
    """Install Soul Forge commands to target platforms."""
    console.print("\n[bold red]🔥 Soul Forge — Initialize[/bold red]\n")

    table = Table(show_header=False)
    for i, p in enumerate(PLATFORMS, 1):
        table.add_row(str(i), p.name)
    console.print(table)

    raw = click.prompt(
        "\nSelect platforms (comma-separated numbers)", type=str
    )
    indices = [int(x.strip()) - 1 for x in raw.split(",") if x.strip().isdigit()]
    selected = [PLATFORMS[i] for i in indices if 0 <= i < len(PLATFORMS)]

    if not selected:
        console.print("[red]No valid platforms selected.[/red]")
        raise SystemExit(1)

    project_dir = Path.cwd()

    for p in selected:
        install_platform(project_dir, p)
        console.print(f"  [green]✅[/green] Installed to {p.commands_path}")

    config = {
        "platforms": [p.id for p in selected],
        "agents_dir": "agents/",
    }
    _save_config(config)
    console.print(f"\n[green]✅[/green] Config saved to {CONFIG_FILE}")
    console.print("[green]✅[/green] agents/ directory created")
    console.print("\n[bold]Done! Use /sf-summon in your AI agent to create characters.[/bold]\n")


@cli.command()
def update():
    """Update commands and sync orchestration blocks."""
    config = _load_config()
    if config is None:
        console.print("[red]No .soul-forge.yaml found. Run 'soul-forge init' first.[/red]")
        raise SystemExit(1)

    project_dir = Path.cwd()
    platforms = get_platforms_by_ids(config.get("platforms", []))

    for p in platforms:
        update_platform(project_dir, p)
        console.print(f"  [green]✅[/green] Updated {p.name}")

    console.print("\n[bold]Update complete.[/bold]\n")


@cli.command()
def platforms():
    """List all supported platforms."""
    table = Table(title="Supported Platforms")
    table.add_column("ID", style="cyan")
    table.add_column("Name")
    table.add_column("Commands Path")
    table.add_column("Config File")

    for p in PLATFORMS:
        table.add_row(p.id, p.name, p.commands_path, p.config_file)

    console.print(table)


from soul_forge.cli_template import template  # noqa: E402

cli.add_command(template)
