# tests/test_integration.py
from pathlib import Path

import yaml
from click.testing import CliRunner

from soul_forge.cli import cli
from soul_forge.managed_block import read_block
from soul_forge.orchestration import generate_orchestration_block


def test_full_workflow(tmp_path: Path, monkeypatch):
    """Test: init -> verify commands -> simulate agent creation -> update -> verify block."""
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
