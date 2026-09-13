from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class Stage:
    name: str
    directory: str
    incar: dict[str, Any]
    kpoints: list[str]


@dataclass(frozen=True)
class Workflow:
    scheduler: str
    job_name: str
    account: str
    queue: str
    walltime: str
    nodes: int
    tasks: int
    memory: str
    module: str
    executable: str
    stages: tuple[Stage, ...]
    source: Path

    @classmethod
    def from_dict(cls, data: dict[str, Any], source: Path) -> "Workflow":
        stages = tuple(Stage(**stage) for stage in data["stages"])
        workflow = cls(stages=stages, source=source, **{k: v for k, v in data.items() if k != "stages"})
        if workflow.scheduler not in {"pbs", "slurm"}:
            raise ValueError("scheduler must be 'pbs' or 'slurm'")
        if not workflow.stages:
            raise ValueError("at least one calculation stage is required")
        return workflow
