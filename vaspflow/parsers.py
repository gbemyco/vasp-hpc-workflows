from __future__ import annotations

import re
from dataclasses import asdict, dataclass
from pathlib import Path

ENERGY = re.compile(r"free\s+energy\s+TOTEN\s*=\s*([-+\d.Ee]+)")
FORCE = re.compile(r"FORCES:\s+max atom, RMS\s*=\s*([-+\d.Ee]+)\s+([-+\d.Ee]+)")


@dataclass
class VaspResult:
    stage: str
    energy_ev: float | None
    max_force_ev_a: float | None
    electronic_converged: bool
    ionic_converged: bool

    def as_dict(self) -> dict[str, object]:
        return asdict(self)


def parse_outcar(path: str | Path, stage: str | None = None) -> VaspResult:
    source = Path(path)
    text = source.read_text(errors="replace")
    energies = ENERGY.findall(text)
    forces = FORCE.findall(text)
    return VaspResult(
        stage=stage or source.parent.name,
        energy_ev=float(energies[-1]) if energies else None,
        max_force_ev_a=float(forces[-1][0]) if forces else None,
        electronic_converged="aborting loop because EDIFF is reached" in text,
        ionic_converged="reached required accuracy" in text,
    )


def workflow_status(root: str | Path) -> list[VaspResult]:
    results = []
    for stage in sorted(Path(root).glob("[0-9][0-9]_*")):
        outcar = stage / "OUTCAR"
        results.append(parse_outcar(outcar, stage.name) if outcar.exists() else VaspResult(stage.name, None, None, False, False))
    return results
