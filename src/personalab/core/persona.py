"""Persona: a virtual user description loaded from a markdown file.

A persona file is plain markdown describing the user's background, goals,
mental state, biases, etc. Optionally the first paragraph can be a YAML-style
frontmatter block (--- ... ---) for structured metadata used by reports.

Example:
    ---
    segment: trader
    archetype: scalper
    hostility: friendly
    ---
    # 01_burnt_veteran

    35 岁的资深加密交易员，过去 3 年订过 6 个信号产品全部退订...
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable


_FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)


@dataclass
class Persona:
    """A virtual user persona loaded from a markdown file.

    Attributes:
        name: stem of the source file (e.g. "01_burnt_veteran")
        content: full markdown source (including any frontmatter)
        body: markdown body with the frontmatter stripped — feed this to the LLM
        path: original file path
        metadata: parsed frontmatter dict (empty if none present)
    """
    name: str
    content: str
    body: str
    path: Path
    metadata: dict = field(default_factory=dict)

    @classmethod
    def from_file(cls, path: Path) -> "Persona":
        content = path.read_text("utf-8")
        meta, body = _split_frontmatter(content)
        return cls(name=path.stem, content=content, body=body,
                   path=path, metadata=meta)


def _split_frontmatter(text: str) -> tuple[dict, str]:
    m = _FRONTMATTER_RE.match(text)
    if not m:
        return {}, text
    raw = m.group(1)
    meta: dict = {}
    for line in raw.splitlines():
        if ":" not in line:
            continue
        k, _, v = line.partition(":")
        meta[k.strip()] = v.strip()
    body = text[m.end():]
    return meta, body


def load_personas(directory: Path | str,
                   filter_names: Iterable[str] | None = None) -> list[Persona]:
    """Load all *.md personas from a directory, sorted by filename.

    If `filter_names` is given, only personas whose stem is in the set are loaded.
    """
    directory = Path(directory)
    if not directory.is_dir():
        raise FileNotFoundError(f"persona dir not found: {directory}")
    files = sorted(directory.glob("*.md"))
    if filter_names is not None:
        wanted = set(filter_names)
        files = [f for f in files if f.stem in wanted]
    return [Persona.from_file(f) for f in files]
