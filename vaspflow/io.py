from __future__ import annotations

import json
from pathlib import Path

from .model import Workflow


def load_workflow(path: str | Path) -> Workflow:
    source = Path(path).resolve()
    with source.open(encoding="utf-8") as handle:
        return Workflow.from_dict(json.load(handle), source)


def write_incar(settings: dict[str, object], destination: Path) -> None:
    lines = [f"{key} = {value}" for key, value in settings.items()]
    destination.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_kpoints(lines: list[str], destination: Path) -> None:
    destination.write_text("\n".join(lines) + "\n", encoding="utf-8")
