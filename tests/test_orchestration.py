from pathlib import Path

import yaml

from soul_forge.orchestration import generate_orchestration_block, parse_agent_frontmatter


AGENT_MAIN = """---
name: main-agent
personality:
  source: preset
  reference: "Default"
expertise: system-architect
role: main
relationship: friend
attitude: null
behavior:
  trigger_mode: auto
---

Main agent prompt.
"""

AGENT_SUB = """---
name: jiraiya-architect
personality:
  source: url
  reference: "Jiraiya — Naruto"
expertise: system-architect
role: sub
relationship: mentor
attitude: null
behavior:
  trigger_mode: auto
trigger:
  conditions:
    - task_type: architecture
  execution_mode: after_main
  output_section: "Architecture Review"
---

Sub agent prompt.
"""

AGENT_MANUAL = """---
name: english-teacher
personality:
  source: preset
  reference: "Default"
expertise: english-teacher
role: sub
relationship: friend
attitude: null
behavior:
  trigger_mode: manual
---

Manual agent prompt.
"""


def test_parse_agent_frontmatter():
    meta = parse_agent_frontmatter(AGENT_SUB)
    assert meta["name"] == "jiraiya-architect"
    assert meta["role"] == "sub"
    assert meta["trigger"]["conditions"] == [{"task_type": "architecture"}]


def test_generate_block_with_main_and_sub(tmp_path: Path):
    agents_dir = tmp_path / "agents"
    agents_dir.mkdir()
    (agents_dir / "main-agent.md").write_text(AGENT_MAIN)
    (agents_dir / "jiraiya-architect.md").write_text(AGENT_SUB)

    block = generate_orchestration_block(agents_dir)
    assert "Main Agent: main-agent" in block
    assert "jiraiya-architect" in block
    assert "task_type:architecture" in block
    assert "after_main" in block


def test_generate_block_no_main(tmp_path: Path):
    agents_dir = tmp_path / "agents"
    agents_dir.mkdir()
    (agents_dir / "jiraiya-architect.md").write_text(AGENT_SUB)

    block = generate_orchestration_block(agents_dir)
    assert "Main Agent: none" in block


def test_generate_block_manual_agents_excluded_from_auto_triggers(tmp_path: Path):
    agents_dir = tmp_path / "agents"
    agents_dir.mkdir()
    (agents_dir / "english-teacher.md").write_text(AGENT_MANUAL)

    block = generate_orchestration_block(agents_dir)
    assert "english-teacher" in block
    assert "manual" in block.lower()


def test_generate_block_empty_dir(tmp_path: Path):
    agents_dir = tmp_path / "agents"
    agents_dir.mkdir()

    block = generate_orchestration_block(agents_dir)
    assert "Main Agent: none" in block
    assert "No sub-agents configured" in block
