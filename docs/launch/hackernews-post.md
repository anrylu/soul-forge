# Hacker News Post Draft

**Title:** Show HN: Soul Forge – RPG-style character creation for AI coding agents

**URL:** https://github.com/anrylu/soul-forge

**Comment:**

Soul Forge lets you create AI agent personas with personality and expertise, then orchestrate them across 5 platforms (Claude Code, Gemini CLI, Codex, GitHub Copilot, OpenCode).

Key design decisions:
- Pure prompt-based: agents are markdown files with YAML frontmatter, no API dependencies
- Declarative triggers: sub-agents activate automatically based on conditions (language detection, code presence, task type)
- Platform-agnostic: single template set deploys to all supported platforms
- Personality/expertise separation: combine any character (fictional or custom) with any expertise role

Install: `uvx soul-forge init`

Built with Python, Click, and Rich. MIT licensed.
