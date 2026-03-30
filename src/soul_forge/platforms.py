from dataclasses import dataclass


@dataclass(frozen=True)
class Platform:
    id: str
    name: str
    commands_path: str
    config_file: str


PLATFORMS: list[Platform] = [
    Platform(id="claude-code", name="Claude Code", commands_path=".claude/commands", config_file="CLAUDE.md"),
    Platform(id="gemini-cli", name="Gemini CLI", commands_path=".gemini/commands", config_file="GEMINI.md"),
    Platform(id="codex", name="Codex", commands_path=".codex/commands", config_file="AGENTS.md"),
    Platform(id="github-copilot", name="GitHub Copilot", commands_path=".github/copilot/commands", config_file=".github/copilot-instructions.md"),
    Platform(id="opencode", name="OpenCode", commands_path=".opencode/commands", config_file="AGENTS.md"),
]


def get_platform(platform_id: str) -> Platform | None:
    for p in PLATFORMS:
        if p.id == platform_id:
            return p
    return None


def get_platforms_by_ids(ids: list[str]) -> list[Platform]:
    return [p for pid in ids if (p := get_platform(pid)) is not None]
