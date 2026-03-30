---
description: "Soul Forge — View your agent party"
---

# Soul Forge — Party

Display all configured agents.

## Instructions

1. Read all `.md` files from `agents/` directory (project-level).
2. Also check `~/.claude/agents/` (global level) if it exists.
3. Parse YAML frontmatter from each.
4. Display as a formatted table:

```
Soul Forge — Party Roster

Name                 | Role | Expertise  | Relation | Trigger              | Location
---------------------|------|------------|----------|----------------------|----------
jiraiya-architect    | sub  | sysarch    | mentor   | auto: task_type:arch | project
english-teacher      | sub  | english    | friend   | auto: contains_eng   | global
vegeta-reviewer      | main | codereview | enemy    | —                    | project

Total: 3 agents (1 main, 2 sub)
```

5. If no agents exist:

```
Your party is empty! Use /sf-summon to forge your first character.
```
