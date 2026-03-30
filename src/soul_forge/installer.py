import importlib.resources
from pathlib import Path
import shutil

from soul_forge.managed_block import write_block
from soul_forge.orchestration import generate_orchestration_block
from soul_forge.platforms import Platform


def _get_template_commands_dir() -> Path:
    return importlib.resources.files("soul_forge") / "templates" / "commands"


def install_platform(project_dir: Path, platform: Platform) -> None:
    commands_dir = project_dir / platform.commands_path
    commands_dir.mkdir(parents=True, exist_ok=True)

    template_dir = _get_template_commands_dir()
    for template_file in sorted(Path(str(template_dir)).glob("sf-*.md")):
        dest = commands_dir / template_file.name
        shutil.copy2(template_file, dest)

    agents_dir = project_dir / "agents"
    agents_dir.mkdir(exist_ok=True)

    config_file = project_dir / platform.config_file
    config_file.parent.mkdir(parents=True, exist_ok=True)
    block_content = generate_orchestration_block(agents_dir)
    write_block(config_file, block_content)


def update_platform(project_dir: Path, platform: Platform) -> None:
    commands_dir = project_dir / platform.commands_path
    commands_dir.mkdir(parents=True, exist_ok=True)

    template_dir = _get_template_commands_dir()
    for template_file in sorted(Path(str(template_dir)).glob("sf-*.md")):
        dest = commands_dir / template_file.name
        shutil.copy2(template_file, dest)

    agents_dir = project_dir / "agents"
    if agents_dir.exists():
        config_file = project_dir / platform.config_file
        block_content = generate_orchestration_block(agents_dir)
        write_block(config_file, block_content)
