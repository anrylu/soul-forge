[English](/README.md) | [繁體中文](/README.zh-tw.md) | [简体中文](/README.zh-cn.md) | [日本語](/README.ja.md)

# Soul Forge

**Summon AI agents with personality.** RPG-style character creation for Claude Code, Gemini CLI, Copilot & more.

[![PyPI version](https://img.shields.io/pypi/v/agentsoulforge)](https://pypi.org/project/agentsoulforge/)
[![Python](https://img.shields.io/pypi/pyversions/agentsoulforge)](https://pypi.org/project/agentsoulforge/)
[![CI](https://github.com/anrylu/soul-forge/actions/workflows/ci.yml/badge.svg)](https://github.com/anrylu/soul-forge/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

<!-- TODO: Replace with actual demo GIF once recorded -->
<!-- ![Demo](docs/assets/demo.gif) -->

## Get Started in 3 Steps

```bash
uvx agentsoulforge init    # Pick your platform
/sf-summon             # Summon your first character
/sf-party              # View your party
```

## Why Soul Forge?

- **Multi-agent orchestration** — One prompt triggers multiple expert agents, each responding in their own style and personality
- **RPG character system** — Manage AI agents like an RPG party: summon, bind, fuse, banish
- **5 platforms, one config** — Claude Code, Gemini CLI, Codex, GitHub Copilot, OpenCode — no vendor lock-in
- **Pure prompt-based** — No API keys, no external services, no runtime dependencies

## See It in Action

Ask: _"幫我寫一個 REST API for user authentication"_ — and your party responds:

| Agent | Personality | Role | What They Do |
|-------|------------|------|-------------|
| **josuke-backend** | Higashikata Josuke (JoJo Part 4) | Backend Dev | Reviews API design, suggests bcrypt + rate limiting |
| **misaka-reviewer** | Misaka Mikoto (Railgun) | Code Reviewer | Spots SQL injection, missing validation, hardcoded secrets |
| **jotaro-sensei** | Jotaro Kujo (JoJo) | Japanese Teacher | Corrects your Japanese grammar |
| **dio-teacher** | DIO (JoJo) | English Teacher | Translates with... dramatic flair |

Each sub-agent activates automatically based on trigger conditions — language detection, code presence, task type, or custom rules.

## Installation

```bash
# Via uvx (recommended, no install needed)
uvx agentsoulforge init

# Or install globally
pip install soul-forge
soul-forge init
```

## Slash Commands

| Command | RPG Meaning | Function |
|---------|-------------|----------|
| `/sf-summon` | Summon | Interactive character creation wizard |
| `/sf-anoint` | Crown | Set an agent as Main Agent |
| `/sf-bind` | Bind | Set an agent as Sub-agent |
| `/sf-engrave` | Engrave runes | Modify trigger conditions |
| `/sf-party` | View party | List all agents |
| `/sf-fuse` | Fuse | Merge two agents into one |
| `/sf-banish` | Banish | Delete an agent |

## How It Works

### Character Creation

`/sf-summon` walks you through a wizard:

1. **Personality Source** — Preset style, URL + character extraction, or custom
2. **Expertise** — Backend, Frontend, DevOps, Code Reviewer, QA, Architect, English/Japanese Teacher, or custom
3. **Naming** — Auto-suggested or custom
4. **Role** — Main Agent or Sub-agent
5. **Relationship** — Mentor, Friend, Enemy, Rival, Servant, Senior, Junior, Partner, or Custom
6. **Response Language** — Auto, Chinese, English, or Japanese
7. **Trigger Mode** — Auto or Manual (sub-agents only)
8. **Fine-tuning** — Optional attitude override
9. **Storage** — Project-level or global

### Agent File Format

Agents are markdown files with YAML frontmatter:

```yaml
---
name: jiraiya-architect
personality:
  source: url
  reference: "Jiraiya — Naruto"
expertise: system-architect
role: sub
relationship: mentor
behavior:
  trigger_mode: auto
trigger:
  conditions:
    - task_type: architecture
  execution_mode: after_main
  output_section: "Architecture Review"
---

You are Jiraiya, the legendary Sannin from Naruto.
# ... personality, expertise, and behavior prompts
```

### Automatic Orchestration

Sub-agents with auto triggers activate based on declarative conditions:

- **Language detection:** `contains_english`, `contains_japanese`, `contains_chinese`
- **Content type:** `contains_code`, `task_type: backend|frontend|devops|architecture`
- **Unconditional:** `always`
- **Custom:** Regex patterns or AI-judged conditions

Execution modes: `after_main`, `before_main`, `parallel`

## Supported Platforms

| Platform | Commands Path | Config File |
|----------|--------------|-------------|
| Claude Code | `.claude/commands/` | `CLAUDE.md` |
| Gemini CLI | `.gemini/commands/` | `GEMINI.md` |
| Codex | `.codex/commands/` | `AGENTS.md` |
| GitHub Copilot | `.github/copilot/commands/` | `.github/copilot-instructions.md` |
| OpenCode | `.opencode/commands/` | `AGENTS.md` |

## Examples

See the [`examples/`](examples/) directory for ready-to-use party configurations:

- [**fullstack-team**](examples/fullstack-team/) — Frontend + Backend + Code Reviewer party
- [**language-tutors**](examples/language-tutors/) — Anime-powered English + Japanese teachers

## Contributing

Contributions welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

The easiest way to contribute is adding new expertise templates — it's just a markdown file!

## Development

```bash
git clone https://github.com/anrylu/soul-forge.git
cd soul-forge
uv venv && uv pip install -e .
uv run pytest -v
```

## License

MIT
