from pathlib import Path

import pytest


@pytest.fixture
def tmp_project(tmp_path: Path) -> Path:
    """Create a temporary project directory."""
    return tmp_path


@pytest.fixture
def sample_agent_md() -> str:
    """Return a sample agent markdown file content."""
    return """---
name: test-agent
personality:
  source: preset
  reference: "Test Personality"
expertise: backend-developer
role: sub
relationship: mentor
attitude: null
behavior:
  trigger_mode: auto
trigger:
  conditions:
    - task_type: backend
  execution_mode: after_main
  output_section: "Backend Review"
---

You are a test agent.

## Personality
- Direct and helpful

## Expertise
You are a Backend Developer specialist.

## Behavior
- As a mentor, you proactively guide and teach
"""
