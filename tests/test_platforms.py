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
