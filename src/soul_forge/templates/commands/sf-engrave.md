---
description: "Soul Forge — Engrave trigger conditions on a Sub-agent"
---

# Soul Forge — Engrave

Modify the trigger conditions for a Sub-agent.

## Instructions

1. Read all `.md` files in `agents/` directory.
2. List only Sub-agents:

```
Soul Forge — Engrave (Modify Triggers)

Sub-agents:
1. jiraiya-architect [auto] triggers: task_type:architecture, runs after_main
2. english-teacher [manual]

Choose which agent to engrave (or 0 to cancel):
```

3. Show current trigger configuration and ask what to change:

```
Current config for {name}:
- Trigger mode: {auto/manual}
- Conditions: {list}
- Execution order: {after_main/before_main/parallel}

What to change?
1. Trigger mode (auto <-> manual)
2. Trigger conditions
3. Execution order
4. All of the above

Choose:
```

4. Walk through the selected changes (reuse the same prompts as /sf-summon Steps 6a-6c).
5. Update the agent file frontmatter.
6. Update orchestration block.
7. Confirm:

```
Runes engraved on {name}!
Orchestration updated.
```
