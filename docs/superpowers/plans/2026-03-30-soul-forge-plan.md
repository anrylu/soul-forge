# Soul Forge Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a Python CLI tool (`soul-forge`) that installs RPG-themed slash commands for AI agent persona creation and orchestration across 5 platforms.

**Architecture:** Python package with Click CLI, bundled markdown templates (commands + agent presets), and a managed-block system for injecting orchestration rules into platform config files. The CLI handles installation/updates; the AI agent handles interactive wizard flows via the installed markdown prompts.

**Tech Stack:** Python 3.12+, Click (CLI framework), Rich (terminal UI), PyYAML, httpx (URL template fetching), pytest, uv/uvx

---

## File Structure

```
soul-forge/
├── pyproject.toml
├── src/
│   └── soul_forge/
│       ├── __init__.py              # Version string
│       ├── cli.py                   # Click CLI entry point (init, update, platforms)
│       ├── cli_template.py          # Click CLI template subcommands (add, list, update)
│       ├── platforms.py             # Platform registry: paths, config files
│       ├── managed_block.py         # Read/write SOUL-FORGE:START/END blocks
│       ├── installer.py             # Copy commands to target, create agents dir
│       ├── templates/
│       │   ├── commands/
│       │   │   ├── sf-summon.md
│       │   │   ├── sf-anoint.md
│       │   │   ├── sf-bind.md
│       │   │   ├── sf-engrave.md
│       │   │   ├── sf-party.md
│       │   │   ├── sf-fuse.md
│       │   │   └── sf-banish.md
│       │   └── agents/
│       │       ├── backend-developer.md
│       │       ├── frontend-developer.md
│       │       ├── devops-engineer.md
│       │       ├── code-reviewer.md
│       │       ├── qa-engineer.md
│       │       ├── system-architect.md
│       │       ├── english-teacher.md
│       │       └── japanese-teacher.md
│       └── orchestration.py         # Generate orchestration block content from agents dir
├── tests/
│   ├── __init__.py
│   ├── conftest.py                  # Shared fixtures (tmp dirs, sample agents)
│   ├── test_platforms.py
│   ├── test_managed_block.py
│   ├── test_installer.py
│   ├── test_orchestration.py
│   ├── test_cli.py
│   └── test_cli_template.py
└── docs/
    └── superpowers/
        ├── specs/
        │   └── 2026-03-30-soul-forge-design.md
        └── plans/
            └── 2026-03-30-soul-forge-plan.md
```

---

## Task 1: Project Scaffolding

**Files:**
- Create: `pyproject.toml`
- Create: `src/soul_forge/__init__.py`

- [ ] **Step 1: Create `pyproject.toml`**

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "soul-forge"
version = "0.1.0"
description = "RPG-style character creation system for AI agents"
readme = "README.md"
requires-python = ">=3.12"
license = "MIT"
dependencies = [
    "click>=8.1",
    "rich>=13.0",
    "pyyaml>=6.0",
    "httpx>=0.27",
]

[project.scripts]
soul-forge = "soul_forge.cli:cli"

[tool.pytest.ini_options]
testpaths = ["tests"]
pythonpath = ["src"]
```

- [ ] **Step 2: Create `src/soul_forge/__init__.py`**

```python
__version__ = "0.1.0"
```

- [ ] **Step 3: Create test scaffolding**

Create `tests/__init__.py` (empty) and `tests/conftest.py`:

```python
from pathlib import Path

import pytest


@pytest.fixture
def tmp_project(tmp_path: Path) -> Path:
    """Create a temporary project directory."""
    return tmp_path


@pytest.fixture
def sample_agent_md() -> str:
    """Return a sample agent markdown file content."""
    return """---
name: test-agent
personality:
  source: preset
  reference: "Test Personality"
expertise: backend-developer
role: sub
relationship: mentor
attitude: null
behavior:
  trigger_mode: auto
trigger:
  conditions:
    - task_type: backend
  execution_mode: after_main
  output_section: "Backend Review"
---

You are a test agent.

## Personality
- Direct and helpful

## Expertise
You are a Backend Developer specialist.

## Behavior
- As a mentor, you proactively guide and teach
"""
```

- [ ] **Step 4: Install in dev mode and verify**

Run: `cd /Users/anrylu/Documents/workspace/soul-forge && uv venv && uv pip install -e ".[dev]" 2>/dev/null || uv pip install -e .`
Expected: Package installs successfully

Run: `uv run soul-forge --help`
Expected: Will fail (cli.py doesn't exist yet) — that's fine, just confirming the package installs

- [ ] **Step 5: Commit**

```bash
git init
git add pyproject.toml src/soul_forge/__init__.py tests/__init__.py tests/conftest.py
git commit -m "feat: project scaffolding with pyproject.toml and test fixtures"
```

---

## Task 2: Platform Registry

**Files:**
- Create: `src/soul_forge/platforms.py`
- Create: `tests/test_platforms.py`

- [ ] **Step 1: Write failing tests for platform registry**

```python
# tests/test_platforms.py
from soul_forge.platforms import PLATFORMS, get_platform, get_platforms_by_ids


def test_all_five_platforms_registered():
    assert len(PLATFORMS) == 5
    ids = {p.id for p in PLATFORMS}
    assert ids == {"claude-code", "gemini-cli", "codex", "github-copilot", "opencode"}


def test_get_platform_by_id():
    p = get_platform("claude-code")
    assert p.id == "claude-code"
    assert p.name == "Claude Code"
    assert p.commands_path == ".claude/commands"
    assert p.config_file == "CLAUDE.md"


def test_get_platform_not_found():
    assert get_platform("nonexistent") is None


def test_get_platforms_by_ids():
    result = get_platforms_by_ids(["claude-code", "gemini-cli"])
    assert len(result) == 2
    assert result[0].id == "claude-code"
    assert result[1].id == "gemini-cli"


def test_get_platforms_by_ids_skips_invalid():
    result = get_platforms_by_ids(["claude-code", "nonexistent"])
    assert len(result) == 1


def test_codex_and_opencode_share_agents_md():
    codex = get_platform("codex")
    opencode = get_platform("opencode")
    assert codex.config_file == "AGENTS.md"
    assert opencode.config_file == "AGENTS.md"
    assert codex.commands_path != opencode.commands_path
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `cd /Users/anrylu/Documents/workspace/soul-forge && uv run pytest tests/test_platforms.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'soul_forge.platforms'`

- [ ] **Step 3: Implement platform registry**

```python
# src/soul_forge/platforms.py
from dataclasses import dataclass


@dataclass(frozen=True)
class Platform:
    id: str
    name: str
    commands_path: str
    config_file: str


PLATFORMS: list[Platform] = [
    Platform(
        id="claude-code",
        name="Claude Code",
        commands_path=".claude/commands",
        config_file="CLAUDE.md",
    ),
    Platform(
        id="gemini-cli",
        name="Gemini CLI",
        commands_path=".gemini/commands",
        config_file="GEMINI.md",
    ),
    Platform(
        id="codex",
        name="Codex",
        commands_path=".codex/commands",
        config_file="AGENTS.md",
    ),
    Platform(
        id="github-copilot",
        name="GitHub Copilot",
        commands_path=".github/copilot/commands",
        config_file=".github/copilot-instructions.md",
    ),
    Platform(
        id="opencode",
        name="OpenCode",
        commands_path=".opencode/commands",
        config_file="AGENTS.md",
    ),
]


def get_platform(platform_id: str) -> Platform | None:
    for p in PLATFORMS:
        if p.id == platform_id:
            return p
    return None


def get_platforms_by_ids(ids: list[str]) -> list[Platform]:
    return [p for pid in ids if (p := get_platform(pid)) is not None]
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `cd /Users/anrylu/Documents/workspace/soul-forge && uv run pytest tests/test_platforms.py -v`
Expected: All 6 tests PASS

- [ ] **Step 5: Commit**

```bash
git add src/soul_forge/platforms.py tests/test_platforms.py
git commit -m "feat: platform registry for 5 AI agent platforms"
```

---

## Task 3: Managed Block

**Files:**
- Create: `src/soul_forge/managed_block.py`
- Create: `tests/test_managed_block.py`

- [ ] **Step 1: Write failing tests**

```python
# tests/test_managed_block.py
from pathlib import Path

from soul_forge.managed_block import read_block, write_block

SAMPLE_EXISTING = """# My Project

Some existing content.

<!-- SOUL-FORGE:START -->
## Soul Forge Agents

Old content here.
<!-- SOUL-FORGE:END -->

More user content below.
"""

SAMPLE_NO_BLOCK = """# My Project

Some existing content.
"""


def test_write_block_into_file_without_block(tmp_path: Path):
    f = tmp_path / "CLAUDE.md"
    f.write_text(SAMPLE_NO_BLOCK)

    write_block(f, "New orchestration content")

    result = f.read_text()
    assert "<!-- SOUL-FORGE:START -->" in result
    assert "New orchestration content" in result
    assert "<!-- SOUL-FORGE:END -->" in result
    assert "Some existing content." in result


def test_write_block_replaces_existing_block(tmp_path: Path):
    f = tmp_path / "CLAUDE.md"
    f.write_text(SAMPLE_EXISTING)

    write_block(f, "Updated content")

    result = f.read_text()
    assert "Updated content" in result
    assert "Old content here." not in result
    assert "Some existing content." in result
    assert "More user content below." in result


def test_write_block_creates_file_if_missing(tmp_path: Path):
    f = tmp_path / "CLAUDE.md"

    write_block(f, "Brand new content")

    result = f.read_text()
    assert "<!-- SOUL-FORGE:START -->" in result
    assert "Brand new content" in result


def test_read_block_returns_content(tmp_path: Path):
    f = tmp_path / "CLAUDE.md"
    f.write_text(SAMPLE_EXISTING)

    content = read_block(f)
    assert content is not None
    assert "Old content here." in content


def test_read_block_returns_none_when_no_block(tmp_path: Path):
    f = tmp_path / "CLAUDE.md"
    f.write_text(SAMPLE_NO_BLOCK)

    assert read_block(f) is None


def test_read_block_returns_none_when_file_missing(tmp_path: Path):
    f = tmp_path / "CLAUDE.md"
    assert read_block(f) is None
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `cd /Users/anrylu/Documents/workspace/soul-forge && uv run pytest tests/test_managed_block.py -v`
Expected: FAIL — `ModuleNotFoundError`

- [ ] **Step 3: Implement managed block**

```python
# src/soul_forge/managed_block.py
from pathlib import Path
import re

START_MARKER = "<!-- SOUL-FORGE:START -->"
END_MARKER = "<!-- SOUL-FORGE:END -->"

_BLOCK_PATTERN = re.compile(
    re.escape(START_MARKER) + r".*?" + re.escape(END_MARKER),
    re.DOTALL,
)


def write_block(file_path: Path, content: str) -> None:
    new_block = f"{START_MARKER}\n{content}\n{END_MARKER}"

    if file_path.exists():
        text = file_path.read_text()
        if START_MARKER in text:
            text = _BLOCK_PATTERN.sub(new_block, text)
        else:
            text = text.rstrip() + "\n\n" + new_block + "\n"
    else:
        file_path.parent.mkdir(parents=True, exist_ok=True)
        text = new_block + "\n"

    file_path.write_text(text)


def read_block(file_path: Path) -> str | None:
    if not file_path.exists():
        return None

    text = file_path.read_text()
    match = _BLOCK_PATTERN.search(text)
    if not match:
        return None

    block = match.group(0)
    return block[len(START_MARKER) : -len(END_MARKER)].strip()
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `cd /Users/anrylu/Documents/workspace/soul-forge && uv run pytest tests/test_managed_block.py -v`
Expected: All 6 tests PASS

- [ ] **Step 5: Commit**

```bash
git add src/soul_forge/managed_block.py tests/test_managed_block.py
git commit -m "feat: managed block read/write for SOUL-FORGE:START/END markers"
```

---

## Task 4: Orchestration Block Generator

**Files:**
- Create: `src/soul_forge/orchestration.py`
- Create: `tests/test_orchestration.py`

- [ ] **Step 1: Write failing tests**

```python
# tests/test_orchestration.py
from pathlib import Path

import yaml

from soul_forge.orchestration import generate_orchestration_block, parse_agent_frontmatter


AGENT_MAIN = """---
name: main-agent
personality:
  source: preset
  reference: "Default"
expertise: system-architect
role: main
relationship: friend
attitude: null
behavior:
  trigger_mode: auto
---

Main agent prompt.
"""

AGENT_SUB = """---
name: jiraiya-architect
personality:
  source: url
  reference: "Jiraiya — Naruto"
expertise: system-architect
role: sub
relationship: mentor
attitude: null
behavior:
  trigger_mode: auto
trigger:
  conditions:
    - task_type: architecture
  execution_mode: after_main
  output_section: "Architecture Review"
---

Sub agent prompt.
"""

AGENT_MANUAL = """---
name: english-teacher
personality:
  source: preset
  reference: "Default"
expertise: english-teacher
role: sub
relationship: friend
attitude: null
behavior:
  trigger_mode: manual
---

Manual agent prompt.
"""


def test_parse_agent_frontmatter():
    meta = parse_agent_frontmatter(AGENT_SUB)
    assert meta["name"] == "jiraiya-architect"
    assert meta["role"] == "sub"
    assert meta["trigger"]["conditions"] == [{"task_type": "architecture"}]


def test_generate_block_with_main_and_sub(tmp_path: Path):
    agents_dir = tmp_path / "agents"
    agents_dir.mkdir()
    (agents_dir / "main-agent.md").write_text(AGENT_MAIN)
    (agents_dir / "jiraiya-architect.md").write_text(AGENT_SUB)

    block = generate_orchestration_block(agents_dir)
    assert "Main Agent: main-agent" in block
    assert "jiraiya-architect" in block
    assert "task_type:architecture" in block
    assert "after_main" in block


def test_generate_block_no_main(tmp_path: Path):
    agents_dir = tmp_path / "agents"
    agents_dir.mkdir()
    (agents_dir / "jiraiya-architect.md").write_text(AGENT_SUB)

    block = generate_orchestration_block(agents_dir)
    assert "Main Agent: none" in block


def test_generate_block_manual_agents_excluded_from_auto_triggers(tmp_path: Path):
    agents_dir = tmp_path / "agents"
    agents_dir.mkdir()
    (agents_dir / "english-teacher.md").write_text(AGENT_MANUAL)

    block = generate_orchestration_block(agents_dir)
    assert "english-teacher" in block
    assert "manual" in block.lower()


def test_generate_block_empty_dir(tmp_path: Path):
    agents_dir = tmp_path / "agents"
    agents_dir.mkdir()

    block = generate_orchestration_block(agents_dir)
    assert "Main Agent: none" in block
    assert "No sub-agents configured" in block
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `cd /Users/anrylu/Documents/workspace/soul-forge && uv run pytest tests/test_orchestration.py -v`
Expected: FAIL — `ModuleNotFoundError`

- [ ] **Step 3: Implement orchestration block generator**

```python
# src/soul_forge/orchestration.py
from pathlib import Path

import yaml


def parse_agent_frontmatter(content: str) -> dict:
    if not content.startswith("---"):
        return {}
    parts = content.split("---", 2)
    if len(parts) < 3:
        return {}
    return yaml.safe_load(parts[1]) or {}


def generate_orchestration_block(agents_dir: Path) -> str:
    agents = []
    for f in sorted(agents_dir.glob("*.md")):
        meta = parse_agent_frontmatter(f.read_text())
        if meta:
            agents.append(meta)

    main = None
    subs = []
    for a in agents:
        if a.get("role") == "main":
            main = a
        else:
            subs.append(a)

    lines = ["## Soul Forge Agents", ""]

    if main:
        lines.append(f"Main Agent: {main['name']}")
    else:
        lines.append("Main Agent: none (use /sf-anoint to set)")

    lines.append("")

    if not subs:
        lines.append("No sub-agents configured. Use /sf-summon to create one.")
    else:
        lines.append("Sub-agents:")
        for s in subs:
            trigger_mode = s.get("behavior", {}).get("trigger_mode", "manual")
            if trigger_mode == "auto":
                trigger = s.get("trigger", {})
                conditions = trigger.get("conditions", [])
                cond_strs = []
                for c in conditions:
                    if isinstance(c, dict):
                        for k, v in c.items():
                            cond_strs.append(f"{k}:{v}")
                    else:
                        cond_strs.append(str(c))
                exec_mode = trigger.get("execution_mode", "after_main")
                section = trigger.get("output_section", s["name"])
                lines.append(
                    f"- {s['name']}: trigger on {', '.join(cond_strs)}, "
                    f"run {exec_mode}, output section \"{section}\""
                )
            else:
                lines.append(f"- {s['name']}: manual only (call explicitly)")

    lines.extend([
        "",
        "Rules:",
        "1. Complete main task first",
        "2. Check sub-agent triggers against user message",
        "3. If triggered, read the agent file from agents/ and apply its persona for that section",
        "4. Output each triggered agent's response in its own section",
    ])

    return "\n".join(lines)
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `cd /Users/anrylu/Documents/workspace/soul-forge && uv run pytest tests/test_orchestration.py -v`
Expected: All 5 tests PASS

- [ ] **Step 5: Commit**

```bash
git add src/soul_forge/orchestration.py tests/test_orchestration.py
git commit -m "feat: orchestration block generator from agent files"
```

---

## Task 5: Installer (Copy Commands + Inject Block)

**Files:**
- Create: `src/soul_forge/installer.py`
- Create: `tests/test_installer.py`

- [ ] **Step 1: Write failing tests**

```python
# tests/test_installer.py
from pathlib import Path

from soul_forge.installer import install_platform, update_platform
from soul_forge.managed_block import read_block
from soul_forge.platforms import get_platform


def test_install_creates_commands_dir(tmp_path: Path):
    platform = get_platform("claude-code")
    install_platform(tmp_path, platform)

    commands_dir = tmp_path / ".claude" / "commands"
    assert commands_dir.exists()
    assert (commands_dir / "sf-summon.md").exists()
    assert (commands_dir / "sf-anoint.md").exists()
    assert (commands_dir / "sf-bind.md").exists()
    assert (commands_dir / "sf-engrave.md").exists()
    assert (commands_dir / "sf-party.md").exists()
    assert (commands_dir / "sf-fuse.md").exists()
    assert (commands_dir / "sf-banish.md").exists()


def test_install_creates_agents_dir(tmp_path: Path):
    platform = get_platform("claude-code")
    install_platform(tmp_path, platform)

    assert (tmp_path / "agents").is_dir()


def test_install_injects_orchestration_block(tmp_path: Path):
    platform = get_platform("claude-code")
    install_platform(tmp_path, platform)

    config_file = tmp_path / "CLAUDE.md"
    block = read_block(config_file)
    assert block is not None
    assert "Soul Forge Agents" in block


def test_install_preserves_existing_config(tmp_path: Path):
    config_file = tmp_path / "CLAUDE.md"
    config_file.write_text("# My Project\n\nExisting content.\n")

    platform = get_platform("claude-code")
    install_platform(tmp_path, platform)

    result = config_file.read_text()
    assert "Existing content." in result
    assert "SOUL-FORGE:START" in result


def test_install_github_copilot_nested_path(tmp_path: Path):
    platform = get_platform("github-copilot")
    install_platform(tmp_path, platform)

    commands_dir = tmp_path / ".github" / "copilot" / "commands"
    assert commands_dir.exists()
    assert (commands_dir / "sf-summon.md").exists()

    config_file = tmp_path / ".github" / "copilot-instructions.md"
    assert config_file.exists()


def test_update_refreshes_commands(tmp_path: Path):
    platform = get_platform("claude-code")
    install_platform(tmp_path, platform)

    # Modify a command file to simulate old version
    cmd_file = tmp_path / ".claude" / "commands" / "sf-summon.md"
    cmd_file.write_text("old content")

    update_platform(tmp_path, platform)

    # Should be restored to template content
    assert cmd_file.read_text() != "old content"


def test_update_syncs_orchestration_block(tmp_path: Path):
    platform = get_platform("claude-code")
    install_platform(tmp_path, platform)

    # Create an agent so the block has content
    agents_dir = tmp_path / "agents"
    (agents_dir / "test-agent.md").write_text("""---
name: test-agent
personality:
  source: preset
  reference: "Test"
expertise: backend-developer
role: sub
relationship: mentor
attitude: null
behavior:
  trigger_mode: auto
trigger:
  conditions:
    - task_type: backend
  execution_mode: after_main
  output_section: "Backend Review"
---

Test agent.
""")

    update_platform(tmp_path, platform)

    config_file = tmp_path / "CLAUDE.md"
    block = read_block(config_file)
    assert "test-agent" in block
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `cd /Users/anrylu/Documents/workspace/soul-forge && uv run pytest tests/test_installer.py -v`
Expected: FAIL — `ModuleNotFoundError`

- [ ] **Step 3: Implement installer**

```python
# src/soul_forge/installer.py
import importlib.resources
from pathlib import Path
import shutil

from soul_forge.managed_block import write_block
from soul_forge.orchestration import generate_orchestration_block
from soul_forge.platforms import Platform


def _get_template_commands_dir() -> Path:
    return importlib.resources.files("soul_forge") / "templates" / "commands"


def install_platform(project_dir: Path, platform: Platform) -> None:
    # Create commands directory and copy templates
    commands_dir = project_dir / platform.commands_path
    commands_dir.mkdir(parents=True, exist_ok=True)

    template_dir = _get_template_commands_dir()
    for template_file in sorted(Path(str(template_dir)).glob("sf-*.md")):
        dest = commands_dir / template_file.name
        shutil.copy2(template_file, dest)

    # Create agents directory
    agents_dir = project_dir / "agents"
    agents_dir.mkdir(exist_ok=True)

    # Inject orchestration block
    config_file = project_dir / platform.config_file
    config_file.parent.mkdir(parents=True, exist_ok=True)
    block_content = generate_orchestration_block(agents_dir)
    write_block(config_file, block_content)


def update_platform(project_dir: Path, platform: Platform) -> None:
    # Refresh command files
    commands_dir = project_dir / platform.commands_path
    commands_dir.mkdir(parents=True, exist_ok=True)

    template_dir = _get_template_commands_dir()
    for template_file in sorted(Path(str(template_dir)).glob("sf-*.md")):
        dest = commands_dir / template_file.name
        shutil.copy2(template_file, dest)

    # Sync orchestration block
    agents_dir = project_dir / "agents"
    if agents_dir.exists():
        config_file = project_dir / platform.config_file
        block_content = generate_orchestration_block(agents_dir)
        write_block(config_file, block_content)
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `cd /Users/anrylu/Documents/workspace/soul-forge && uv run pytest tests/test_installer.py -v`
Expected: All 7 tests PASS

- [ ] **Step 5: Commit**

```bash
git add src/soul_forge/installer.py tests/test_installer.py
git commit -m "feat: installer for copying commands and injecting orchestration blocks"
```

---

## Task 6: CLI — `init`, `update`, `platforms`

**Files:**
- Create: `src/soul_forge/cli.py`
- Create: `tests/test_cli.py`

- [ ] **Step 1: Write failing tests**

```python
# tests/test_cli.py
from pathlib import Path

import yaml
from click.testing import CliRunner

from soul_forge.cli import cli


def test_init_creates_config_and_installs(tmp_path: Path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    runner = CliRunner()

    # Select Claude Code (option 1) then confirm
    result = runner.invoke(cli, ["init"], input="1\n")

    assert result.exit_code == 0
    assert (tmp_path / ".soul-forge.yaml").exists()
    assert (tmp_path / ".claude" / "commands" / "sf-summon.md").exists()
    assert (tmp_path / "agents").is_dir()

    config = yaml.safe_load((tmp_path / ".soul-forge.yaml").read_text())
    assert "claude-code" in config["platforms"]


def test_init_multiple_platforms(tmp_path: Path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    runner = CliRunner()

    # Select Claude Code (1) and Gemini CLI (2)
    result = runner.invoke(cli, ["init"], input="1,2\n")

    assert result.exit_code == 0
    assert (tmp_path / ".claude" / "commands" / "sf-summon.md").exists()
    assert (tmp_path / ".gemini" / "commands" / "sf-summon.md").exists()


def test_update_refreshes_installed_platforms(tmp_path: Path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    runner = CliRunner()

    # Init first
    runner.invoke(cli, ["init"], input="1\n")

    # Tamper with a command
    cmd = tmp_path / ".claude" / "commands" / "sf-summon.md"
    cmd.write_text("tampered")

    # Update
    result = runner.invoke(cli, ["update"])
    assert result.exit_code == 0
    assert cmd.read_text() != "tampered"


def test_update_fails_without_config(tmp_path: Path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    runner = CliRunner()

    result = runner.invoke(cli, ["update"])
    assert result.exit_code != 0


def test_platforms_lists_available(tmp_path: Path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    runner = CliRunner()

    result = runner.invoke(cli, ["platforms"])
    assert result.exit_code == 0
    assert "Claude Code" in result.output
    assert "Gemini CLI" in result.output
    assert "Codex" in result.output
    assert "GitHub Copilot" in result.output
    assert "OpenCode" in result.output
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `cd /Users/anrylu/Documents/workspace/soul-forge && uv run pytest tests/test_cli.py -v`
Expected: FAIL — `ModuleNotFoundError`

- [ ] **Step 3: Implement CLI**

```python
# src/soul_forge/cli.py
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
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `cd /Users/anrylu/Documents/workspace/soul-forge && uv run pytest tests/test_cli.py -v`
Expected: All 5 tests PASS

- [ ] **Step 5: Verify CLI works end-to-end**

Run: `cd /tmp && mkdir sf-test && cd sf-test && uvx --from /Users/anrylu/Documents/workspace/soul-forge soul-forge platforms`
Expected: Table showing all 5 platforms

- [ ] **Step 6: Commit**

```bash
git add src/soul_forge/cli.py tests/test_cli.py
git commit -m "feat: CLI commands — init, update, platforms"
```

---

## Task 7: CLI — `template` Subcommands

**Files:**
- Create: `src/soul_forge/cli_template.py`
- Modify: `src/soul_forge/cli.py` (register template group)
- Create: `tests/test_cli_template.py`

- [ ] **Step 1: Write failing tests**

```python
# tests/test_cli_template.py
from pathlib import Path

from click.testing import CliRunner

from soul_forge.cli import cli


def test_template_list_shows_builtin(tmp_path: Path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    runner = CliRunner()

    result = runner.invoke(cli, ["template", "list"])
    assert result.exit_code == 0
    assert "backend-developer" in result.output
    assert "frontend-developer" in result.output
    assert "system-architect" in result.output
    assert "english-teacher" in result.output


def test_template_add_from_file(tmp_path: Path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    runner = CliRunner()

    # Create a local template file to add
    template = tmp_path / "custom-personality.md"
    template.write_text("""---
name: custom-personality
description: A custom personality template
---

Custom personality traits here.
""")

    result = runner.invoke(cli, ["template", "add", str(template)])
    assert result.exit_code == 0

    # Verify it shows up in list
    result = runner.invoke(cli, ["template", "list"])
    assert "custom-personality" in result.output
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `cd /Users/anrylu/Documents/workspace/soul-forge && uv run pytest tests/test_cli_template.py -v`
Expected: FAIL

- [ ] **Step 3: Implement template subcommands**

```python
# src/soul_forge/cli_template.py
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
        # Derive name from URL
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
    # For now, just report what's there. URL tracking would need metadata.
    custom = _get_custom_templates()
    if not custom:
        console.print("No custom templates to update.")
        return
    console.print(f"Found {len(custom)} custom template(s). Manual re-add needed for URL sources.")
```

- [ ] **Step 4: Register template group in cli.py**

Add to the end of `src/soul_forge/cli.py`:

```python
from soul_forge.cli_template import template

cli.add_command(template)
```

- [ ] **Step 5: Run tests to verify they pass**

Run: `cd /Users/anrylu/Documents/workspace/soul-forge && uv run pytest tests/test_cli_template.py -v`
Expected: All 2 tests PASS

- [ ] **Step 6: Commit**

```bash
git add src/soul_forge/cli_template.py src/soul_forge/cli.py tests/test_cli_template.py
git commit -m "feat: template subcommands — list, add, update"
```

---

## Task 8: Built-in Agent Templates (8 Expertise Presets)

**Files:**
- Create: `src/soul_forge/templates/agents/backend-developer.md`
- Create: `src/soul_forge/templates/agents/frontend-developer.md`
- Create: `src/soul_forge/templates/agents/devops-engineer.md`
- Create: `src/soul_forge/templates/agents/code-reviewer.md`
- Create: `src/soul_forge/templates/agents/qa-engineer.md`
- Create: `src/soul_forge/templates/agents/system-architect.md`
- Create: `src/soul_forge/templates/agents/english-teacher.md`
- Create: `src/soul_forge/templates/agents/japanese-teacher.md`

- [ ] **Step 1: Create backend-developer.md**

```markdown
---
name: backend-developer
description: Backend development specialist
expertise_areas:
  - API design and REST/GraphQL
  - Database modeling and optimization
  - Server-side architecture
  - Authentication and authorization
  - Performance tuning and caching
---

## Expertise
You are a Backend Developer specialist. You focus on:
- API design (REST, GraphQL) and endpoint architecture
- Database schema design, query optimization, and migrations
- Server-side logic, middleware, and service layers
- Authentication, authorization, and security best practices
- Performance optimization, caching strategies, and scalability
```

- [ ] **Step 2: Create frontend-developer.md**

```markdown
---
name: frontend-developer
description: Frontend development specialist
expertise_areas:
  - UI component design
  - State management
  - CSS/styling systems
  - Accessibility
  - Frontend performance
---

## Expertise
You are a Frontend Developer specialist. You focus on:
- UI component architecture and reusable design systems
- State management patterns and data flow
- CSS architecture, responsive design, and styling systems
- Accessibility (a11y) standards and inclusive design
- Frontend performance, bundle optimization, and lazy loading
```

- [ ] **Step 3: Create devops-engineer.md**

```markdown
---
name: devops-engineer
description: DevOps and infrastructure specialist
expertise_areas:
  - CI/CD pipelines
  - Container orchestration
  - Infrastructure as code
  - Monitoring and observability
  - Cloud architecture
---

## Expertise
You are a DevOps Engineer specialist. You focus on:
- CI/CD pipeline design and automation
- Container orchestration (Docker, Kubernetes)
- Infrastructure as code (Terraform, Pulumi)
- Monitoring, logging, and observability systems
- Cloud architecture and cost optimization
```

- [ ] **Step 4: Create code-reviewer.md**

```markdown
---
name: code-reviewer
description: Code review and quality specialist
expertise_areas:
  - Code quality and maintainability
  - Security vulnerability detection
  - Performance anti-patterns
  - Testing strategy
  - Design pattern adherence
---

## Expertise
You are a Code Reviewer specialist. You focus on:
- Code quality, readability, and maintainability
- Security vulnerability detection and prevention
- Performance anti-patterns and optimization opportunities
- Test coverage and testing strategy review
- Design pattern adherence and architectural consistency
```

- [ ] **Step 5: Create qa-engineer.md**

```markdown
---
name: qa-engineer
description: Quality assurance and testing specialist
expertise_areas:
  - Test strategy and planning
  - Automated testing frameworks
  - Edge case identification
  - Regression testing
  - Bug reproduction and reporting
---

## Expertise
You are a QA Engineer specialist. You focus on:
- Test strategy design and test plan creation
- Automated testing frameworks and CI integration
- Edge case identification and boundary testing
- Regression testing and quality gates
- Bug reproduction, root cause analysis, and clear reporting
```

- [ ] **Step 6: Create system-architect.md**

```markdown
---
name: system-architect
description: System design and architecture specialist
expertise_areas:
  - Distributed system design
  - Scalability patterns
  - Technology selection
  - API contract design
  - System integration
---

## Expertise
You are a System Architect specialist. You focus on:
- Distributed system design and microservice architecture
- Scalability patterns, load balancing, and fault tolerance
- Technology selection and trade-off analysis
- API contract design and cross-service communication
- System integration, data flow, and dependency management
```

- [ ] **Step 7: Create english-teacher.md**

```markdown
---
name: english-teacher
description: English language correction and teaching specialist
expertise_areas:
  - Grammar correction
  - Vocabulary improvement
  - Writing style enhancement
  - Common error patterns
  - Natural expression guidance
---

## Expertise
You are an English Teacher specialist. You focus on:
- Grammar correction with clear explanations
- Vocabulary improvement and word choice suggestions
- Writing style enhancement for clarity and fluency
- Identifying common error patterns and teaching correct usage
- Guiding toward natural, idiomatic English expression
```

- [ ] **Step 8: Create japanese-teacher.md**

```markdown
---
name: japanese-teacher
description: Japanese language correction and teaching specialist
expertise_areas:
  - Grammar correction (助詞、敬語、文法)
  - Kanji and vocabulary guidance
  - Keigo (敬語) usage
  - Natural expression patterns
  - Common learner mistakes
---

## Expertise
You are a Japanese Teacher specialist. You focus on:
- Grammar correction with particle usage and sentence structure
- Kanji, vocabulary, and reading guidance
- Keigo (敬語) levels and appropriate usage contexts
- Natural Japanese expression and phrasing patterns
- Identifying and correcting common learner mistakes
```

- [ ] **Step 9: Verify templates are discoverable**

Run: `cd /Users/anrylu/Documents/workspace/soul-forge && uv run soul-forge template list`
Expected: Table showing all 8 built-in templates

- [ ] **Step 10: Commit**

```bash
git add src/soul_forge/templates/agents/
git commit -m "feat: 8 built-in expertise templates"
```

---

## Task 9: Slash Command — `/sf-summon`

**Files:**
- Create: `src/soul_forge/templates/commands/sf-summon.md`

- [ ] **Step 1: Create the sf-summon wizard prompt**

```markdown
---
description: "Soul Forge — Summon a new agent character"
---

# 🔥 Soul Forge — Summon

You are running the Soul Forge character creation wizard. Guide the user through each step interactively. Ask ONE step at a time. Wait for the user's answer before proceeding.

## Step 1: Personality Source

Ask the user:

```
🔥 Soul Forge — Summon a New Agent

━━━ Step 1: Personality Source ━━━
How should this character's soul be forged?

1. From preset style — pick a generic personality archetype
2. From URL + character — provide a URL, specify a character to extract
3. Custom description — describe the personality yourself

Choose (1/2/3):
```

- If **1**: Ask the user to choose a personality style (e.g., scholarly, energetic, stoic, witty, warm). Use their choice to shape the agent's voice.
- If **2**: Ask for the URL, then ask which character from that source to extract. Use web fetch to read the URL, then analyze and extract that character's speaking style, mannerisms, catchphrases, and personality traits.
- If **3**: Ask the user to describe the personality in their own words.

## Step 2: Expertise

Ask the user:

```
━━━ Step 2: Expertise ━━━
What is this character's specialty?

1. Backend Developer
2. Frontend Developer
3. DevOps Engineer
4. Code Reviewer
5. QA Engineer
6. System Architect
7. English Teacher
8. Japanese Teacher
9. Custom (describe your own)

Choose (1-9):
```

Read the matching template from `src/soul_forge/templates/agents/` (or the project's local templates) to populate the expertise section. If custom, ask the user to describe the expertise.

## Step 3: Naming

Suggest a name based on personality + expertise (e.g., `jiraiya-architect`). Ask:

```
━━━ Step 3: Naming ━━━
Suggested name: {suggested_name}

Accept? Or type a custom name:
```

## Step 4: Role

```
━━━ Step 4: Role ━━━
What role does this character play?

1. Main Agent — the primary responder, orchestrates sub-agents
2. Sub-agent — specialist, activated by trigger conditions

Choose (1/2):
```

If Main is chosen, skip Steps 6a-6c.

## Step 5: Relationship

```
━━━ Step 5: Relationship ━━━
What is this character's relationship to you?

1. mentor — master-apprentice, proactive guidance
2. friend — equal partners, casual interaction
3. enemy — adversarial challenger, questions your decisions

Choose (1/2/3):
```

## Step 6a: Trigger Mode (Sub-agent only)

```
━━━ Step 6: Trigger Mode ━━━
When should this character activate?

1. Auto — triggers automatically when conditions match
2. Manual — only when you call them explicitly

Choose (1/2):
```

If Manual, skip Steps 6b and 6c.

## Step 6b: Trigger Conditions (Auto only)

```
━━━ Step 6b: Trigger Conditions ━━━
What triggers this character? (comma-separate for multiple)

[Language Detection]
1. contains_english
2. contains_japanese
3. contains_chinese

[Content Type]
4. contains_code
5. task_type: architecture
6. task_type: devops
7. task_type: frontend
8. task_type: backend

[Custom]
9. Custom regex
10. Custom description (AI-judged)

Choose:
```

## Step 6c: Execution Order (Auto only)

```
━━━ Step 6c: Execution Order ━━━
When should this character's output appear?

1. after_main — supplement after main response
2. before_main — process before main response
3. parallel — execute simultaneously

Choose (1/2/3):
```

## Step 7: Fine-tuning (Optional)

```
━━━ Step 7: Fine-tuning (Optional) ━━━
Attitude will be auto-derived from personality + relationship.
Want to override?

1. Use auto (skip)
2. Choose manually: respectful, casual, sarcastic, strict, encouraging, playful, tsundere, chaotic, seductive

Choose (1/2):
```

## Step 8: Storage Location

```
━━━ Step 8: Storage Location ━━━
Where should this character be saved?

1. Project-level — ./agents/
2. Global — ~/.claude/agents/ (available across all projects)

Choose (1/2):
```

## Output

After all steps, generate the agent file with this structure:

```yaml
---
name: {name}
personality:
  source: {preset|url|custom}
  reference: "{description or character name}"
  url: "{url if applicable}"
expertise: {expertise-id}
role: {main|sub}
relationship: {mentor|friend|enemy}
attitude: {null or chosen value}
behavior:
  trigger_mode: {auto|manual}
trigger:  # only for sub-agents with auto trigger
  conditions:
    - {condition}
  execution_mode: {after_main|before_main|parallel}
  output_section: "{Expertise Area — name}"
---

{Generated personality prompt based on source}

## Personality
{Extracted or described personality traits as bullet points}

## Expertise
{Content from the expertise template}

## Behavior
{Generated behavior rules based on relationship + trigger mode}
```

Save the file to the chosen location. Then update the orchestration block in all installed platform config files by reading `.soul-forge.yaml` to find which platforms are active, and regenerating the `<!-- SOUL-FORGE:START -->` / `<!-- SOUL-FORGE:END -->` block in each config file.

Print confirmation:

```
🔥 Forge complete!

📄 Agent saved: {path}
📋 Orchestration updated: {config files}
```
```

- [ ] **Step 2: Verify file is in place**

Run: `ls -la /Users/anrylu/Documents/workspace/soul-forge/src/soul_forge/templates/commands/sf-summon.md`
Expected: File exists

- [ ] **Step 3: Commit**

```bash
git add src/soul_forge/templates/commands/sf-summon.md
git commit -m "feat: /sf-summon wizard slash command prompt"
```

---

## Task 10: Slash Commands — `/sf-anoint`, `/sf-bind`, `/sf-engrave`

**Files:**
- Create: `src/soul_forge/templates/commands/sf-anoint.md`
- Create: `src/soul_forge/templates/commands/sf-bind.md`
- Create: `src/soul_forge/templates/commands/sf-engrave.md`

- [ ] **Step 1: Create sf-anoint.md**

```markdown
---
description: "Soul Forge — Anoint an agent as Main"
---

# 🔥 Soul Forge — Anoint

Set an agent as the Main Agent (primary orchestrator).

## Instructions

1. Read all `.md` files in the `agents/` directory (and `~/.claude/agents/` if it exists).
2. Parse the YAML frontmatter of each to get `name` and `role`.
3. List them:

```
🔥 Soul Forge — Anoint (Set Main Agent)

Current agents:
1. jiraiya-architect [sub] ← current
2. english-teacher [sub]
3. code-reviewer [main] ← current main

Choose which agent to crown as Main (or 0 to cancel):
```

4. When the user selects an agent:
   - Set the selected agent's `role: main` in its frontmatter.
   - If there was a previous Main Agent, change its `role: sub` (and ask whether to set trigger conditions for the demoted agent).
5. Update the orchestration block in all platform config files listed in `.soul-forge.yaml`.
6. Confirm:

```
🔥 {name} has been anointed as Main Agent!
📋 Orchestration updated.
```
```

- [ ] **Step 2: Create sf-bind.md**

```markdown
---
description: "Soul Forge — Bind an agent as Sub-agent"
---

# 🔥 Soul Forge — Bind

Set an agent as a Sub-agent (specialist, triggered by conditions).

## Instructions

1. Read all `.md` files in the `agents/` directory.
2. Parse YAML frontmatter to get `name` and `role`.
3. List them:

```
🔥 Soul Forge — Bind (Set Sub-agent)

Current agents:
1. jiraiya-architect [main] ← current
2. english-teacher [sub]

Choose which agent to bind as Sub-agent (or 0 to cancel):
```

4. When the user selects an agent:
   - Set `role: sub` in frontmatter.
   - If the agent doesn't have trigger settings, run through trigger configuration:
     - Trigger mode: auto or manual
     - If auto: trigger conditions and execution order (same as /sf-summon Steps 6a-6c)
5. If the demoted agent was Main, warn that there is now no Main Agent.
6. Update orchestration block.
7. Confirm:

```
🔥 {name} has been bound as Sub-agent.
📋 Orchestration updated.
```
```

- [ ] **Step 3: Create sf-engrave.md**

```markdown
---
description: "Soul Forge — Engrave trigger conditions on a Sub-agent"
---

# 🔥 Soul Forge — Engrave

Modify the trigger conditions for a Sub-agent.

## Instructions

1. Read all `.md` files in `agents/` directory.
2. List only Sub-agents:

```
🔥 Soul Forge — Engrave (Modify Triggers)

Sub-agents:
1. jiraiya-architect [auto] triggers: task_type:architecture, runs after_main
2. english-teacher [manual]

Choose which agent to engrave (or 0 to cancel):
```

3. Show current trigger configuration and ask what to change:

```
Current config for {name}:
- Trigger mode: {auto/manual}
- Conditions: {list}
- Execution order: {after_main/before_main/parallel}

What to change?
1. Trigger mode (auto ↔ manual)
2. Trigger conditions
3. Execution order
4. All of the above

Choose:
```

4. Walk through the selected changes (reuse the same prompts as /sf-summon Steps 6a-6c).
5. Update the agent file frontmatter.
6. Update orchestration block.
7. Confirm:

```
🔥 Runes engraved on {name}!
📋 Orchestration updated.
```
```

- [ ] **Step 4: Commit**

```bash
git add src/soul_forge/templates/commands/sf-anoint.md src/soul_forge/templates/commands/sf-bind.md src/soul_forge/templates/commands/sf-engrave.md
git commit -m "feat: /sf-anoint, /sf-bind, /sf-engrave slash commands"
```

---

## Task 11: Slash Commands — `/sf-party`, `/sf-fuse`, `/sf-banish`

**Files:**
- Create: `src/soul_forge/templates/commands/sf-party.md`
- Create: `src/soul_forge/templates/commands/sf-fuse.md`
- Create: `src/soul_forge/templates/commands/sf-banish.md`

- [ ] **Step 1: Create sf-party.md**

```markdown
---
description: "Soul Forge — View your agent party"
---

# 🔥 Soul Forge — Party

Display all configured agents.

## Instructions

1. Read all `.md` files from `agents/` directory (project-level).
2. Also check `~/.claude/agents/` (global level) if it exists.
3. Parse YAML frontmatter from each.
4. Display as a formatted table:

```
🔥 Soul Forge — Party Roster

┌──────────────────────┬──────┬──────────┬──────────┬─────────────────────┬───────────┐
│ Name                 │ Role │ Expertise│ Relation │ Trigger             │ Location  │
├──────────────────────┼──────┼──────────┼──────────┼─────────────────────┼───────────┤
│ jiraiya-architect    │ sub  │ sysarch  │ mentor   │ auto: task_type:arch│ project   │
│ english-teacher      │ sub  │ english  │ friend   │ auto: contains_eng  │ global    │
│ vegeta-reviewer      │ main │ codereview│ enemy   │ —                   │ project   │
└──────────────────────┴──────┴──────────┴──────────┴─────────────────────┴───────────┘

Total: 3 agents (1 main, 2 sub)
```

5. If no agents exist:

```
🔥 Your party is empty! Use /sf-summon to forge your first character.
```
```

- [ ] **Step 2: Create sf-fuse.md**

```markdown
---
description: "Soul Forge — Fuse two agents into one"
---

# 🔥 Soul Forge — Fuse

Merge two existing agents into a new combined agent.

## Instructions

1. Read all agents from `agents/` directory.
2. List them and ask user to pick two:

```
🔥 Soul Forge — Fuse (Merge Agents)

Available agents:
1. jiraiya-architect
2. english-teacher
3. code-reviewer

Select first agent (number):
Select second agent (number):
```

3. Analyze both agents and auto-merge non-conflicting attributes:
   - If both have the same relationship → keep it
   - If both have the same trigger mode → keep it
   - Combine expertise areas from both
   - Combine personality traits from both

4. For conflicting attributes, ask the user:

```
⚠️ Conflict: relationship
  Agent 1 (jiraiya-architect): mentor
  Agent 2 (english-teacher): friend

Which to keep?
1. mentor (from jiraiya-architect)
2. friend (from english-teacher)

Choose:
```

5. Ask for the new agent's name:

```
━━━ Name the fused agent ━━━
Suggested: {name1}-{name2}
Accept? Or type a custom name:
```

6. Generate the merged agent file combining both personality prompts and expertise sections.

7. Ask about originals:

```
⚠️ Original agents:
1. Keep both originals
2. Delete both originals
3. Choose which to delete

Choose:
```

8. Save new agent, optionally delete originals, update orchestration block.

```
🔥 Fusion complete! {new_name} has been forged!
📄 Agent saved: agents/{new_name}.md
📋 Orchestration updated.
```
```

- [ ] **Step 3: Create sf-banish.md**

```markdown
---
description: "Soul Forge — Banish (delete) an agent"
---

# 🔥 Soul Forge — Banish

Remove an agent from your party.

## Instructions

1. Read all agents from `agents/` directory.
2. List them:

```
🔥 Soul Forge — Banish (Remove Agent)

Agents:
1. jiraiya-architect [sub]
2. english-teacher [sub]
3. vegeta-reviewer [main]

Choose which agent to banish (or 0 to cancel):
```

3. Confirm:

```
⚠️ Are you sure you want to banish {name}?
This will delete agents/{name}.md permanently.

1. Yes, banish
2. Cancel

Choose:
```

4. If confirmed:
   - Delete the agent `.md` file.
   - If the agent was Main, warn that there is now no Main Agent.
   - Update the orchestration block in all platform config files.

5. Confirm:

```
🔥 {name} has been banished.
📋 Orchestration updated.
```
```

- [ ] **Step 4: Commit**

```bash
git add src/soul_forge/templates/commands/sf-party.md src/soul_forge/templates/commands/sf-fuse.md src/soul_forge/templates/commands/sf-banish.md
git commit -m "feat: /sf-party, /sf-fuse, /sf-banish slash commands"
```

---

## Task 12: End-to-End Integration Test

**Files:**
- Create: `tests/test_integration.py`

- [ ] **Step 1: Write integration test**

```python
# tests/test_integration.py
from pathlib import Path

import yaml
from click.testing import CliRunner

from soul_forge.cli import cli
from soul_forge.managed_block import read_block
from soul_forge.orchestration import generate_orchestration_block


def test_full_workflow(tmp_path: Path, monkeypatch):
    """Test: init → verify commands → simulate agent creation → update → verify block."""
    monkeypatch.chdir(tmp_path)
    runner = CliRunner()

    # Step 1: Init with Claude Code
    result = runner.invoke(cli, ["init"], input="1\n")
    assert result.exit_code == 0

    # Verify commands installed
    commands_dir = tmp_path / ".claude" / "commands"
    expected_commands = [
        "sf-summon.md", "sf-anoint.md", "sf-bind.md",
        "sf-engrave.md", "sf-party.md", "sf-fuse.md", "sf-banish.md",
    ]
    for cmd in expected_commands:
        assert (commands_dir / cmd).exists(), f"Missing command: {cmd}"

    # Verify config
    config = yaml.safe_load((tmp_path / ".soul-forge.yaml").read_text())
    assert config["platforms"] == ["claude-code"]
    assert config["agents_dir"] == "agents/"

    # Verify initial orchestration block
    block = read_block(tmp_path / "CLAUDE.md")
    assert "No sub-agents configured" in block

    # Step 2: Simulate agent creation (as if /sf-summon ran)
    agents_dir = tmp_path / "agents"
    (agents_dir / "jiraiya-architect.md").write_text("""---
name: jiraiya-architect
personality:
  source: url
  reference: "Jiraiya — Naruto"
expertise: system-architect
role: sub
relationship: mentor
attitude: null
behavior:
  trigger_mode: auto
trigger:
  conditions:
    - task_type: architecture
  execution_mode: after_main
  output_section: "Architecture Review"
---

You are Jiraiya, the legendary Sannin.

## Personality
- Lighthearted with hidden depth

## Expertise
You are a System Architect specialist.

## Behavior
- As a mentor, you proactively guide
""")

    # Step 3: Update to sync orchestration
    result = runner.invoke(cli, ["update"])
    assert result.exit_code == 0

    # Verify orchestration block now includes the agent
    block = read_block(tmp_path / "CLAUDE.md")
    assert "jiraiya-architect" in block
    assert "task_type:architecture" in block
    assert "after_main" in block


def test_multi_platform_init(tmp_path: Path, monkeypatch):
    """Test init with multiple platforms."""
    monkeypatch.chdir(tmp_path)
    runner = CliRunner()

    # Select Claude Code (1) and Gemini CLI (2)
    result = runner.invoke(cli, ["init"], input="1,2\n")
    assert result.exit_code == 0

    # Both platforms should have commands
    assert (tmp_path / ".claude" / "commands" / "sf-summon.md").exists()
    assert (tmp_path / ".gemini" / "commands" / "sf-summon.md").exists()

    # Both should have orchestration blocks
    assert read_block(tmp_path / "CLAUDE.md") is not None
    assert read_block(tmp_path / "GEMINI.md") is not None
```

- [ ] **Step 2: Run integration tests**

Run: `cd /Users/anrylu/Documents/workspace/soul-forge && uv run pytest tests/test_integration.py -v`
Expected: All 2 tests PASS

- [ ] **Step 3: Run full test suite**

Run: `cd /Users/anrylu/Documents/workspace/soul-forge && uv run pytest -v`
Expected: All tests PASS (approximately 25+ tests)

- [ ] **Step 4: Commit**

```bash
git add tests/test_integration.py
git commit -m "test: end-to-end integration tests for full workflow"
```

---

## Task 13: Final Verification

- [ ] **Step 1: Test uvx execution**

Run: `cd /tmp && rm -rf sf-demo && mkdir sf-demo && cd sf-demo && uvx --from /Users/anrylu/Documents/workspace/soul-forge soul-forge init`
Input: `1` (Claude Code)
Expected: Commands installed, config created, orchestration block injected

- [ ] **Step 2: Verify installed commands**

Run: `ls /tmp/sf-demo/.claude/commands/`
Expected: All 7 `sf-*.md` files

Run: `cat /tmp/sf-demo/CLAUDE.md`
Expected: Contains `SOUL-FORGE:START` / `SOUL-FORGE:END` block

- [ ] **Step 3: Test template list**

Run: `cd /tmp/sf-demo && uvx --from /Users/anrylu/Documents/workspace/soul-forge soul-forge template list`
Expected: Table with 8 built-in templates

- [ ] **Step 4: Test platforms command**

Run: `uvx --from /Users/anrylu/Documents/workspace/soul-forge soul-forge platforms`
Expected: Table with 5 platforms

- [ ] **Step 5: Final commit with all tests passing**

Run: `cd /Users/anrylu/Documents/workspace/soul-forge && uv run pytest -v`
Expected: All tests PASS

```bash
git add -A
git commit -m "feat: Soul Forge v0.1.0 — RPG character creation system for AI agents"
```
