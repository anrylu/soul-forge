from pathlib import Path

from soul_forge.managed_block import read_block, write_block

SAMPLE_EXISTING = """# My Project

Some existing content.

<!-- SOUL-FORGE:START -->
## Soul Forge Agents

Old content here.
<!-- SOUL-FORGE:END -->

More user content below.
"""

SAMPLE_NO_BLOCK = """# My Project

Some existing content.
"""


def test_write_block_into_file_without_block(tmp_path: Path):
    f = tmp_path / "CLAUDE.md"
    f.write_text(SAMPLE_NO_BLOCK)
    write_block(f, "New orchestration content")
    result = f.read_text()
    assert "<!-- SOUL-FORGE:START -->" in result
    assert "New orchestration content" in result
    assert "<!-- SOUL-FORGE:END -->" in result
    assert "Some existing content." in result


def test_write_block_replaces_existing_block(tmp_path: Path):
    f = tmp_path / "CLAUDE.md"
    f.write_text(SAMPLE_EXISTING)
    write_block(f, "Updated content")
    result = f.read_text()
    assert "Updated content" in result
    assert "Old content here." not in result
    assert "Some existing content." in result
    assert "More user content below." in result


def test_write_block_creates_file_if_missing(tmp_path: Path):
    f = tmp_path / "CLAUDE.md"
    write_block(f, "Brand new content")
    result = f.read_text()
    assert "<!-- SOUL-FORGE:START -->" in result
    assert "Brand new content" in result


def test_read_block_returns_content(tmp_path: Path):
    f = tmp_path / "CLAUDE.md"
    f.write_text(SAMPLE_EXISTING)
    content = read_block(f)
    assert content is not None
    assert "Old content here." in content


def test_read_block_returns_none_when_no_block(tmp_path: Path):
    f = tmp_path / "CLAUDE.md"
    f.write_text(SAMPLE_NO_BLOCK)
    assert read_block(f) is None


def test_read_block_returns_none_when_file_missing(tmp_path: Path):
    f = tmp_path / "CLAUDE.md"
    assert read_block(f) is None
