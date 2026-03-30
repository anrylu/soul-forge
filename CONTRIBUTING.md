# Contributing to Soul Forge

Thanks for your interest in contributing!

## Quick Start

```bash
git clone https://github.com/anrylu/soul-forge.git
cd soul-forge
uv venv
uv pip install -e .
uv run pytest -v
```

## Ways to Contribute

### Add an Expertise Template (Easiest!)

Expertise templates are markdown files in `src/soul_forge/templates/agents/`. To add one:

1. Create a new `.md` file in `src/soul_forge/templates/agents/`
2. Use this format:

```yaml
---
name: your-template-name
description: One-line description
expertise_areas:
  - Area 1
  - Area 2
  - Area 3
---

## Expertise
You are a [Role] specialist. You focus on:
- Skill 1
- Skill 2
- Skill 3
```

3. Open a PR with the new file.

### Report Bugs

Open an issue using the Bug Report template. Include:
- What you did
- What you expected
- What happened instead
- Your platform (Claude Code, Gemini CLI, etc.)

### Suggest Features

Open an issue using the Feature Request template.

## Pull Request Guidelines

1. Fork the repo and create a branch from `master`
2. Add tests if you're adding functionality
3. Make sure `uv run pytest -v` passes
4. Keep PRs focused — one feature or fix per PR

## Code Style

- Python 3.12+
- Type hints encouraged
- Run tests before submitting: `uv run pytest -v`
