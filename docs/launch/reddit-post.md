# Reddit Post Draft

**Subreddits:** r/ClaudeAI, r/ChatGPTCoding

**Title:** I built an RPG party system for AI coding agents — summon characters with personality across Claude Code, Gemini, Copilot & more

**Body:**

I got tired of plain system prompts, so I built **Soul Forge** — an RPG-style character creation system for AI coding agents.

**What it does:**
- `/sf-summon` walks you through creating an agent with personality (any fictional character) + expertise (backend dev, code reviewer, etc.)
- Sub-agents trigger automatically based on what you're doing — writing backend code, making grammar mistakes, etc.
- Works across Claude Code, Gemini CLI, Codex, GitHub Copilot, and OpenCode

**Example:** I have Jotaro Kujo as my Japanese teacher (triggers on Japanese text), DIO as my English teacher (triggers on English), and Misaka Mikoto as my code reviewer (triggers on code). They all respond in character.

```bash
uvx soul-forge init    # Pick your platform
/sf-summon             # Summon your first character
/sf-party              # View your party
```

Pure prompt-based — no API keys, no external services. Just markdown files with YAML frontmatter.

GitHub: https://github.com/anrylu/soul-forge

Would love feedback! The easiest way to contribute is adding new expertise templates (it's just a markdown file).
