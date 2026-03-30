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
    template = tmp_path / "custom-personality.md"
    template.write_text("""---
name: custom-personality
description: A custom personality template
---

Custom personality traits here.
""")
    result = runner.invoke(cli, ["template", "add", str(template)])
    assert result.exit_code == 0
    result = runner.invoke(cli, ["template", "list"])
    assert "custom-personality" in result.output
