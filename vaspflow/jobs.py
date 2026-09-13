from __future__ import annotations

import json
import shutil
from pathlib import Path

from .io import write_incar, write_kpoints
from .model import Workflow


PBS = """#!/bin/bash
#PBS -N {job_name}
#PBS -A {account}
#PBS -q {queue}
#PBS -l walltime={walltime}
#PBS -l ncpus={tasks}
#PBS -l mem={memory}
#PBS -j oe
set -euo pipefail
cd "$PBS_O_WORKDIR"
module load {module}
{restart}
mpirun -np {tasks} {executable} > vasp.stdout
"""

SLURM = """#!/bin/bash
#SBATCH --job-name={job_name}
#SBATCH --account={account}
#SBATCH --partition={queue}
#SBATCH --time={walltime}
#SBATCH --nodes={nodes}
#SBATCH --ntasks={tasks}
#SBATCH --mem={memory}
#SBATCH --output=vasp.%j.out
set -euo pipefail
module load {module}
{restart}
srun {executable} > vasp.stdout
"""


def _restart_command(previous: str | None) -> str:
    if previous is None:
        return "# First stage: POSCAR is supplied with the example."
    return f'test -s "../{previous}/CONTCAR" && cp "../{previous}/CONTCAR" POSCAR'


def generate(workflow: Workflow, output: Path) -> list[Path]:
    output.mkdir(parents=True, exist_ok=True)
    template = PBS if workflow.scheduler == "pbs" else SLURM
    previous: str | None = None
    created: list[Path] = []
    example_root = workflow.source.parent
    for index, stage in enumerate(workflow.stages, start=1):
        folder = output / f"{index:02d}_{stage.directory}"
        folder.mkdir(parents=True, exist_ok=True)
        write_incar(stage.incar, folder / "INCAR")
        write_kpoints(stage.kpoints, folder / "KPOINTS")
        poscar = example_root / "POSCAR"
        if index == 1 and poscar.exists():
            shutil.copy2(poscar, folder / "POSCAR")
        values = {
            **workflow.__dict__,
            "job_name": f"{workflow.job_name}-{stage.name}",
            "restart": _restart_command(previous),
        }
        (folder / "submit.sh").write_text(template.format_map(values), encoding="utf-8")
        (folder / "stage.json").write_text(json.dumps({"name": stage.name, "index": index}, indent=2) + "\n", encoding="utf-8")
        created.append(folder)
        previous = folder.name
    return created
