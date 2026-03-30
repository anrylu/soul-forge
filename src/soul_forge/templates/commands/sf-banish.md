---
description: "Soul Forge — Banish (delete) an agent"
---

# Soul Forge — Banish

Remove an agent from your party.

## Instructions

1. Read all agents from `agents/` directory.
2. List them:

```
Soul Forge — Banish (Remove Agent)

Agents:
1. jiraiya-architect [sub]
2. english-teacher [sub]
3. vegeta-reviewer [main]

Choose which agent to banish (or 0 to cancel):
```

3. Confirm:

```
Are you sure you want to banish {name}?
This will delete agents/{name}.md permanently.

1. Yes, banish
2. Cancel

Choose:
```

4. If confirmed:
   - Delete the agent `.md` file.
   - If the agent was Main, warn that there is now no Main Agent.
   - Update the orchestration block in all platform config files.

5. Confirm:

```
{name} has been banished.
Orchestration updated.
```
