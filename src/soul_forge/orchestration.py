from pathlib import Path

import yaml


def parse_agent_frontmatter(content: str) -> dict:
    if not content.startswith("---"):
        return {}
    parts = content.split("---", 2)
    if len(parts) < 3:
        return {}
    return yaml.safe_load(parts[1]) or {}


def generate_orchestration_block(agents_dir: Path) -> str:
    agents = []
    for f in sorted(agents_dir.glob("*.md")):
        meta = parse_agent_frontmatter(f.read_text())
        if meta:
            agents.append(meta)

    main = None
    subs = []
    for a in agents:
        if a.get("role") == "main":
            main = a
        else:
            subs.append(a)

    lines = ["## Soul Forge Agents", ""]

    if main:
        lines.append(f"Main Agent: {main['name']}")
    else:
        lines.append("Main Agent: none (use /sf-anoint to set)")

    lines.append("")

    if not subs:
        lines.append("No sub-agents configured. Use /sf-summon to create one.")
    else:
        lines.append("Sub-agents:")
        for s in subs:
            trigger_mode = s.get("behavior", {}).get("trigger_mode", "manual")
            if trigger_mode == "auto":
                trigger = s.get("trigger", {})
                conditions = trigger.get("conditions", [])
                cond_strs = []
                for c in conditions:
                    if isinstance(c, dict):
                        for k, v in c.items():
                            cond_strs.append(f"{k}:{v}")
                    else:
                        cond_strs.append(str(c))
                exec_mode = trigger.get("execution_mode", "after_main")
                section = trigger.get("output_section", s["name"])
                lines.append(
                    f"- {s['name']}: trigger on {', '.join(cond_strs)}, "
                    f"run {exec_mode}, output section \"{section}\""
                )
            else:
                lines.append(f"- {s['name']}: manual only (call explicitly)")

    lines.extend([
        "",
        "Rules:",
        "1. Complete main task first",
        "2. Check sub-agent triggers against user message",
        "3. If triggered, read the agent file from agents/ and apply its persona for that section",
        "4. Output each triggered agent's response in its own section",
    ])

    return "\n".join(lines)
