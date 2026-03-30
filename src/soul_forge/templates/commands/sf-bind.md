---
description: "Soul Forge — Bind an agent as Sub-agent"
---

# Soul Forge — Bind

Set an agent as a Sub-agent (specialist, triggered by conditions).

## Instructions

1. Read all `.md` files in the `agents/` directory.
2. Parse YAML frontmatter to get `name` and `role`.
3. List them:

```
Soul Forge — Bind (Set Sub-agent)

Current agents:
1. jiraiya-architect [main]
2. english-teacher [sub]

Choose which agent to bind as Sub-agent (or 0 to cancel):
```

4. When the user selects an agent:
   - Set `role: sub` in frontmatter.
   - If the agent doesn't have trigger settings, run through trigger configuration:
     - Trigger mode: auto or manual
     - If auto: trigger conditions and execution order (same as /sf-summon Steps 6a-6c)
5. If the demoted agent was Main, warn that there is now no Main Agent.
6. Update orchestration block.
7. Confirm:

```
{name} has been bound as Sub-agent.
Orchestration updated.
```
