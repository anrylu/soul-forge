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

    always_agents = []

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
                has_always = False
                for c in conditions:
                    if isinstance(c, dict):
                        for k, v in c.items():
                            cond_strs.append(f"{k}:{v}")
                    elif c == "always":
                        has_always = True
                        cond_strs.append("always")
                    else:
                        cond_strs.append(str(c))
                exec_mode = trigger.get("execution_mode", "after_main")
                section = trigger.get("output_section", s["name"])
                if has_always:
                    always_agents.append(s["name"])
                    lines.append(
                        f"- {s['name']}: **ALWAYS trigger on EVERY message**, "
                        f"run {exec_mode}, output section \"{section}\""
                    )
                else:
                    lines.append(
                        f"- {s['name']}: trigger on {', '.join(cond_strs)}, "
                        f"run {exec_mode}, output section \"{section}\""
                    )
            else:
                lines.append(f"- {s['name']}: manual only (call explicitly)")

    lines.extend([
        "",
        "Rules (MANDATORY — you MUST follow these for every response):",
        "1. Complete main task first",
        "2. Check EVERY sub-agent trigger condition against the user message",
        "3. If triggered, read the agent file from agents/ and apply its persona for that section",
        "4. Output each triggered agent's response in its own clearly separated section",
        "5. NEVER skip a triggered sub-agent — if the condition matches, the agent MUST appear",
    ])

    if always_agents:
        names = ", ".join(always_agents)
        lines.extend([
            "",
            f"IMPORTANT: The following agents have 'always' triggers and MUST appear in EVERY response without exception: {names}",
            "Do NOT skip them even if they seem irrelevant to the current message.",
        ])

    return "\n".join(lines)
