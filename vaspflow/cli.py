from __future__ import annotations

import argparse
import csv
from pathlib import Path

from .io import load_workflow
from .jobs import generate
from .parsers import workflow_status
from .thermo import hydrogen_adsorption_free_energy


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="vaspflow")
    sub = parser.add_subparsers(dest="command", required=True)
    make = sub.add_parser("generate", help="generate staged inputs and job scripts")
    make.add_argument("config")
    make.add_argument("--output", required=True)
    status = sub.add_parser("status", help="show calculation status")
    status.add_argument("root")
    collect = sub.add_parser("collect", help="collect results into CSV")
    collect.add_argument("root")
    collect.add_argument("--csv", required=True)
    her = sub.add_parser("her", help="calculate hydrogen adsorption free energy")
    her.add_argument("--clean", type=float, required=True)
    her.add_argument("--adsorbed", type=float, required=True)
    her.add_argument("--h2", type=float, required=True)
    her.add_argument("--zpe-correction", type=float, default=0.0)
    her.add_argument("--entropy-correction", type=float, default=0.0)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    if args.command == "generate":
        folders = generate(load_workflow(args.config), Path(args.output))
        print(f"Generated {len(folders)} stages in {args.output}")
    elif args.command == "status":
        for result in workflow_status(args.root):
            print(f"{result.stage:20} E={result.energy_ev!s:>14} electronic={result.electronic_converged} ionic={result.ionic_converged}")
    elif args.command == "collect":
        rows = [result.as_dict() for result in workflow_status(args.root)]
        with Path(args.csv).open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(rows[0]) if rows else ["stage"])
            writer.writeheader()
            writer.writerows(rows)
        print(f"Wrote {len(rows)} rows to {args.csv}")
    elif args.command == "her":
        value = hydrogen_adsorption_free_energy(args.clean, args.adsorbed, args.h2, args.zpe_correction, args.entropy_correction)
        print(f"Delta G_H* = {value:.4f} eV")
    return 0
