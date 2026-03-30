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
    cmd_file = tmp_path / ".claude" / "commands" / "sf-summon.md"
    cmd_file.write_text("old content")
    update_platform(tmp_path, platform)
    assert cmd_file.read_text() != "old content"


def test_update_syncs_orchestration_block(tmp_path: Path):
    platform = get_platform("claude-code")
    install_platform(tmp_path, platform)
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
