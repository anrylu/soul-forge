# Soul Forge — Design Spec

## Overview

Soul Forge is an RPG-style character creation system for AI agents. It lets users create, configure, and orchestrate AI agent personas through an interactive wizard, with automatic multi-agent collaboration via declarative trigger rules.

**Core concept:** Personality + Expertise + Relationship + Triggers = a fully configured AI agent that can be summoned, bound, fused, or banished.

## Architecture

### Python CLI Tool (`soul-forge`)

A Python package executable via `uvx soul-forge`. Responsible for:

- Installing slash command files to target AI agent platforms
- Managing orchestration blocks in platform config files
- Managing agent templates (built-in and URL-sourced)

### Slash Commands (Markdown Prompts)

The actual wizard and management interactions run inside the AI agent (Claude Code, Gemini CLI, etc.) via platform-native slash commands. The CLI installs these as `.md` files.

### Agent Files (Generated Output)

Created agents are stored as `.md` files with YAML frontmatter (structured data) + markdown body (prompt).

## Supported Platforms

| Platform | Commands Path | Config File (orchestration block) |
|----------|--------------|-----------------------------------|
| Claude Code | `.claude/commands/` | `CLAUDE.md` |
| Gemini CLI | `.gemini/commands/` | `GEMINI.md` |
| Codex | `.codex/commands/` | `AGENTS.md` |
| GitHub Copilot | `.github/copilot/commands/` | `.github/copilot-instructions.md` |
| OpenCode | `.opencode/commands/` | `AGENTS.md` |

> **Note:** Codex and OpenCode both use `AGENTS.md`. When both are installed, they share the same orchestration block in `AGENTS.md`. The managed block markers ensure safe coexistence — commands are installed to separate directories (`.codex/` vs `.opencode/`), only the config file is shared.

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

## `/sf-summon` Wizard Flow

### Step 1: Personality Source

How the agent's "soul" is created:

1. **From preset style** — generic personality templates (no expertise attached)
2. **From URL + character extraction** — provide a URL/article, specify a character (real person, anime, novel, movie character), extract their speaking style and mannerisms
3. **Custom description** — user describes personality traits directly

### Step 2: Expertise

What the agent is good at. Independent from personality.

Options:
- Backend Developer
- Frontend Developer
- DevOps Engineer
- Code Reviewer
- QA Engineer
- System Architect
- English Teacher
- Japanese Teacher
- Custom (user describes)

**Example:** Personality = Jiraiya (Naruto), Expertise = System Architect. Result: Jiraiya's speaking style teaching you system architecture.

### Step 3: Naming

Auto-suggest based on personality + expertise (e.g., `jiraiya-architect`). User can accept or customize.

### Step 4: Role

- **Main Agent** — orchestrates sub-agents, handles primary responses
- **Sub-agent** — specialist, triggered by conditions

### Step 5: Relationship

- **mentor** — master-apprentice dynamic, proactive guidance
- **friend** — equal partners, casual interaction
- **enemy** — adversarial challenger, questions your decisions
- **rival** — competitive peer, pushes you to be better
- **servant** — loyal subordinate, fully obedient
- **senior** — experienced elder, respectful but assertive
- **junior** — eager learner, humble and curious
- **partner** — complementary collaborator, fills your gaps
- **custom** — user describes the relationship dynamic in their own words

### Step 5b: Response Language

- **auto** — match the language of the conversation (default)
- **zh** — Chinese
- **en** — English
- **ja** — Japanese

**Language teacher exception:** English Teacher and Japanese Teacher ignore this setting. They follow special rules:
- If the conversation is in their target language → correct and teach
- If the conversation is NOT in their target language → explain how to translate into their language

### Step 6: Trigger Mode (Sub-agent only)

- **Auto** — triggers automatically when conditions are met
- **Manual** — only responds when explicitly called

### Step 6b: Trigger Conditions (Auto mode only)

Available conditions:

**Language detection:**
- `contains_english`
- `contains_japanese`
- `contains_chinese`

**Content type:**
- `contains_code`
- `task_type: architecture`
- `task_type: devops`
- `task_type: frontend`
- `task_type: backend`

**Always:**
- `always` — trigger on every message

**Custom:**
- Custom regex
- Custom description (AI-judged)

### Step 6c: Execution Order (Auto mode only)

- `after_main` — supplement after main response
- `before_main` — process before main response
- `parallel` — execute simultaneously

### Step 7: Fine-tuning (Optional)

Attitude is auto-derived from personality + relationship by default. User can optionally override with:

- respectful, casual, sarcastic, strict, encouraging, playful, tsundere, chaotic, seductive

### Step 8: Storage Location

- **Project-level** — `./agents/`
- **Global** — `~/.claude/agents/` (or platform equivalent)

Project-level takes priority over global.

## Agent File Format

```markdown
---
name: jiraiya-architect
personality:
  source: url
  reference: "Jiraiya — Naruto"
  url: "https://naruto.fandom.com/wiki/Jiraiya"
expertise: system-architect
role: sub
relationship: mentor
relationship_description: null  # only used when relationship is "custom"
response_language: auto  # auto|zh|en|ja
attitude: null  # auto-derived unless user overrides
behavior:
  trigger_mode: auto
trigger:
  conditions:
    - task_type: architecture
  execution_mode: after_main
  output_section: "Architecture Review"
---

You are Jiraiya, the legendary Sannin from Naruto.

## Personality
- Speaks casually with hidden depth
- Teaches through metaphors, occasionally goes off-topic
- Lighthearted on the surface, deadly serious when it matters

## Expertise
You are a System Architect specialist. You focus on:
- System design and architecture decisions
- Scalability and performance trade-offs
- Technology selection recommendations

## Behavior
- As a mentor, you proactively guide and teach
- Point out architecture issues without being asked
- Explain technical concepts in Jiraiya's voice
```

## Orchestration via Managed Block

`soul-forge init` injects a managed block into the platform config file (e.g., `CLAUDE.md`):

```markdown
<!-- SOUL-FORGE:START -->
## Soul Forge Agents

Main Agent: none (use /sf-anoint to set)

Sub-agents:
- jiraiya-architect: trigger on task_type:architecture, run after_main
- english-teacher: trigger on contains_english, run after_main

Rules:
1. Complete main task first
2. Check sub-agent triggers against user message
3. If triggered, read the agent file and apply its persona for that section
4. Output each triggered agent's response in its own section
<!-- SOUL-FORGE:END -->
```

This block is automatically updated whenever agents are created, modified, or deleted via any `/sf-*` command.

## `/sf-fuse` Merge Behavior

1. Analyze both agents
2. Auto-merge non-conflicting attributes
3. For conflicts, interactively ask user which to keep
4. Name the new merged agent
5. Optionally delete or keep original agents
6. Update orchestration block

## CLI Tool (`soul-forge`)

### Commands

| Command | Description |
|---------|-------------|
| `soul-forge init` | Interactive platform selection, install commands, create agents dir, inject orchestration block |
| `soul-forge update` | Update commands and sync orchestration block for all installed platforms |
| `soul-forge template add <url>` | Download and cache a personality/expertise template from URL |
| `soul-forge template list` | List built-in and custom templates |
| `soul-forge template update` | Re-fetch all URL-sourced templates |
| `soul-forge platforms` | List installed platforms |

### Configuration File

`.soul-forge.yaml` at project root:

```yaml
platforms:
  - claude-code
  - gemini-cli
agents_dir: agents/
```

### Template Storage

- Built-in templates: bundled in the Python package under `src/soul_forge/templates/`
- Custom templates: stored in `~/.soul-forge/templates/`

### Project Structure

```
soul-forge/                          # Python package source
├── pyproject.toml                   # Package config, uvx-executable
├── src/
│   └── soul_forge/
│       ├── __init__.py
│       ├── cli.py                   # CLI entry point
│       ├── platforms.py             # Platform-specific path/config logic
│       ├── templates/
│       │   ├── commands/            # Slash command prompts
│       │   │   ├── sf-summon.md
│       │   │   ├── sf-anoint.md
│       │   │   ├── sf-bind.md
│       │   │   ├── sf-engrave.md
│       │   │   ├── sf-party.md
│       │   │   ├── sf-fuse.md
│       │   │   └── sf-banish.md
│       │   └── agents/             # Built-in agent templates
│       │       ├── backend-developer.md
│       │       ├── frontend-developer.md
│       │       ├── devops-engineer.md
│       │       ├── code-reviewer.md
│       │       ├── qa-engineer.md
│       │       ├── system-architect.md
│       │       ├── english-teacher.md
│       │       └── japanese-teacher.md
│       └── managed_block.py        # SOUL-FORGE:START/END block management
└── docs/
    └── superpowers/
        └── specs/
            └── 2026-03-30-soul-forge-design.md
```

## Output Format

When multiple agents are triggered, output is structured in sections:

```
[Main Response]
Your system can be designed like this...

---

[Architecture Review — jiraiya-architect]
Heh, not bad kid. But let me tell you about scalability...

---

[English Correction — english-teacher]
❌ I want design system
✅ I want to design a system
```

## Key Design Decisions

1. **Personality ≠ Expertise** — A character's soul (Jiraiya) is independent from their skill (System Architect)
2. **Attitude is derived** — Personality + Relationship auto-determines attitude; optional override available
3. **Pure Prompt approach** — All wizard interactions are markdown prompts executed by the AI agent, not custom UI
4. **Managed blocks** — Orchestration rules are injected into platform config files with safe update markers
5. **Dual storage** — Project-level (`./agents/`) and global (`~/.claude/agents/`) with project-level priority
6. **Multi-platform** — Single source of truth (templates), output adapted per platform
