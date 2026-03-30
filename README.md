# Soul Forge

RPG-style character creation system for AI agents. Create, configure, and orchestrate AI agent personas with personality, expertise, and automatic trigger-based collaboration.

## Features

- **RPG Character Creation** — Interactive wizard to forge agent personas with personality + expertise
- **Multi-Agent Orchestration** — Main agent + sub-agents with declarative trigger conditions
- **Multi-Platform Support** — Claude Code, Gemini CLI, Codex, GitHub Copilot, OpenCode
- **Personality Sources** — Preset styles, URL/character extraction, or custom descriptions
- **8 Built-in Expertise Templates** — Backend, Frontend, DevOps, Code Review, QA, Architecture, English, Japanese

## Quick Start

```bash
# Install to your project
uvx soul-forge init

# Select your AI agent platform(s), then use slash commands:
/sf-summon     # Create a new agent character
/sf-party      # View your agent roster
```

## Installation

```bash
# Via uvx (recommended)
uvx soul-forge init

# Or install globally
pip install soul-forge
soul-forge init
```

## CLI Commands

| Command | Description |
|---------|-------------|
| `soul-forge init` | Install commands to target platform(s) |
| `soul-forge update` | Update commands and sync orchestration |
| `soul-forge platforms` | List supported platforms |
| `soul-forge template list` | List available templates |
| `soul-forge template add <url\|path>` | Add a custom template |

## Slash Commands

Once installed, these commands are available in your AI agent:

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

### 1. Create an Agent

`/sf-summon` walks you through an 8-step wizard:

1. **Personality Source** — Preset style, URL + character extraction, or custom
2. **Expertise** — Backend Dev, Frontend Dev, DevOps, Code Reviewer, QA, Architect, English/Japanese Teacher, or custom
3. **Naming** — Auto-suggested or custom
4. **Role** — Main Agent or Sub-agent
5. **Relationship** — Mentor, Friend, Enemy, Rival, Servant, Senior, Junior, Partner, or Custom
6. **Response Language** — Auto (match conversation), Chinese, English, or Japanese
7. **Trigger Mode** — Auto or Manual (sub-agents only)
8. **Fine-tuning** — Optional attitude override
9. **Storage** — Project-level or global

### 2. Automatic Orchestration

Sub-agents with auto triggers activate based on conditions:

```
[Main Response]
Your system can be designed like this...

---

[Architecture Review — jiraiya-architect]
Heh, not bad kid. But let me tell you about scalability...

---

[English Correction — english-teacher]
"I want design system" -> "I want to design a system"
```

### 3. Agent File Format

Agents are stored as markdown files with YAML frontmatter:

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

## Supported Platforms

| Platform | Commands Path | Config File |
|----------|--------------|-------------|
| Claude Code | `.claude/commands/` | `CLAUDE.md` |
| Gemini CLI | `.gemini/commands/` | `GEMINI.md` |
| Codex | `.codex/commands/` | `AGENTS.md` |
| GitHub Copilot | `.github/copilot/commands/` | `.github/copilot-instructions.md` |
| OpenCode | `.opencode/commands/` | `AGENTS.md` |

## Development

```bash
git clone https://github.com/your-username/soul-forge.git
cd soul-forge
uv venv && uv pip install -e .
uv run pytest -v
```

## License

MIT
