---
description: "Soul Forge — Anoint an agent as Main"
---

# Soul Forge — Anoint

Set an agent as the Main Agent (primary orchestrator).

## Instructions

1. Read all `.md` files in the `agents/` directory (and `~/.claude/agents/` if it exists).
2. Parse the YAML frontmatter of each to get `name` and `role`.
3. List them:

```
Soul Forge — Anoint (Set Main Agent)

Current agents:
1. jiraiya-architect [sub]
2. english-teacher [sub]
3. code-reviewer [main] <- current main

Choose which agent to crown as Main (or 0 to cancel):
```

4. When the user selects an agent:
   - Set the selected agent's `role: main` in its frontmatter.
   - If there was a previous Main Agent, change its `role: sub` (and ask whether to set trigger conditions for the demoted agent).
5. Update the orchestration block in all platform config files listed in `.soul-forge.yaml`.
6. Confirm:

```
{name} has been anointed as Main Agent!
Orchestration updated.
```
