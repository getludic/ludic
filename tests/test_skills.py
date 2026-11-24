"""The Python examples in the agent skills must run.

Coding agents copy these examples, so an example using an API that does not
exist teaches them to write code that fails. Every ``python`` code block in
``skills/*/SKILL.md`` runs on its own, with its own imports.
"""

import re
from collections.abc import Iterator
from pathlib import Path
from typing import Any

import pytest

SKILLS_DIR = Path(__file__).parent.parent / "skills"
PYTHON_BLOCK = re.compile(r"^```python\n(.*?)^```", re.DOTALL | re.MULTILINE)


def python_blocks() -> Iterator[Any]:
    for path in sorted(SKILLS_DIR.glob("*/SKILL.md")):
        text = path.read_text()
        for match in PYTHON_BLOCK.finditer(text):
            line = text.count("\n", 0, match.start()) + 1
            name = f"{path.relative_to(SKILLS_DIR.parent)}:{line}"
            yield pytest.param(name, match.group(1), id=name)


def test_skills_have_python_examples() -> None:
    assert len(list(python_blocks())) >= 10


@pytest.mark.parametrize(("name", "code"), python_blocks())
def test_skill_example_runs(name: str, code: str) -> None:
    exec(compile(code, name, "exec"), {"__name__": "skill_example"})  # noqa: S102
