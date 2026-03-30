from pathlib import Path

import yaml
from click.testing import CliRunner

from soul_forge.cli import cli


def test_init_creates_config_and_installs(tmp_path: Path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    runner = CliRunner()
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
    result = runner.invoke(cli, ["init"], input="1,2\n")
    assert result.exit_code == 0
    assert (tmp_path / ".claude" / "commands" / "sf-summon.md").exists()
    assert (tmp_path / ".gemini" / "commands" / "sf-summon.md").exists()


def test_update_refreshes_installed_platforms(tmp_path: Path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    runner = CliRunner()
    runner.invoke(cli, ["init"], input="1\n")
    cmd = tmp_path / ".claude" / "commands" / "sf-summon.md"
    cmd.write_text("tampered")
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
