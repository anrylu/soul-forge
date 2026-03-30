---
description: "Soul Forge — Fuse two agents into one"
---

# Soul Forge — Fuse

Merge two existing agents into a new combined agent.

## Instructions

1. Read all agents from `agents/` directory.
2. List them and ask user to pick two:

```
Soul Forge — Fuse (Merge Agents)

Available agents:
1. jiraiya-architect
2. english-teacher
3. code-reviewer

Select first agent (number):
Select second agent (number):
```

3. Analyze both agents and auto-merge non-conflicting attributes:
   - If both have the same relationship -> keep it
   - If both have the same trigger mode -> keep it
   - Combine expertise areas from both
   - Combine personality traits from both

4. For conflicting attributes, ask the user:

```
Conflict: relationship
  Agent 1 (jiraiya-architect): mentor
  Agent 2 (english-teacher): friend

Which to keep?
1. mentor (from jiraiya-architect)
2. friend (from english-teacher)

Choose:
```

5. Ask for the new agent's name:

```
Name the fused agent
Suggested: {name1}-{name2}
Accept? Or type a custom name:
```

6. Generate the merged agent file combining both personality prompts and expertise sections.

7. Ask about originals:

```
Original agents:
1. Keep both originals
2. Delete both originals
3. Choose which to delete

Choose:
```

8. Save new agent, optionally delete originals, update orchestration block.

```
Fusion complete! {new_name} has been forged!
Agent saved: agents/{new_name}.md
Orchestration updated.
```
