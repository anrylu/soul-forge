[English](/README.md) | [繁體中文](/README.zh-tw.md) | [简体中文](/README.zh-cn.md) | [日本語](/README.ja.md)

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

### 2. Example Party

Here's what a team of anime-powered agents might look like:

| Agent | Personality | Expertise | Relationship | Trigger |
|-------|------------|-----------|--------------|---------|
| jotaro-sensei | Jotaro Kujo (JoJo's Bizarre Adventure) | Japanese Teacher | mentor | `contains_japanese` |
| dio-teacher | DIO (JoJo's Bizarre Adventure) | English Teacher | enemy | `contains_english` |
| josuke-backend | Higashikata Josuke (JoJo Part 4) | Backend Developer | friend | `task_type: backend` |
| misaka-reviewer | Misaka Mikoto (A Certain Scientific Railgun) | Code Reviewer | rival | `contains_code` |

### 3. Automatic Orchestration

Sub-agents with auto triggers activate based on conditions. Imagine you ask: "幫我寫一個 REST API for user authentication"

```
[Main Response]
Here's the REST API design for user authentication...

---

[Backend Review — josuke-backend]
グレートだぜ！But let me fix this up real nice.
Your auth endpoint should use bcrypt for password hashing,
and don't forget rate limiting on /login...

---

[Code Review — misaka-reviewer]
Hmph, not bad... but I found 3 issues. Don't think I'm
doing this for you or anything.
1. SQL injection risk in the query builder
2. Missing input validation on email format
3. JWT secret should come from env, not hardcoded

---

[Japanese — jotaro-sensei]
「幫我寫」は中国語だな。日本語では：
「ユーザー認証用のREST APIを書いてください」
やれやれだぜ... 「寫」じゃなくて「書いて」だ。

---

[English — dio-teacher]
You thought you could write English without me, DIO?
MUDA MUDA MUDA!
"Help me write a REST API for user authentication"
- "Help me write" not "幫我寫" — you SHALL speak English!
```

### 4. Agent File Format

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
git clone https://github.com/anrylu/soul-forge.git
cd soul-forge
uv venv && uv pip install -e .
uv run pytest -v
```

## License

MIT
