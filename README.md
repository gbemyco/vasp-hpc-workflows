# VASP HPC Workflows

A small, auditable workflow generator for staged VASP calculations on PBS Pro and
SLURM clusters. It demonstrates the practical automation patterns I use in
computational materials research: reproducible inputs, explicit dependencies,
restart-aware job scripts, lightweight output parsing, and provenance capture.

The repository contains no licensed VASP files (`POTCAR`) and no unpublished
research structures or energies. The bundled silicon example and output snippets
are synthetic and are intended only to exercise the workflow.

## What it demonstrates

- Multi-stage `relax -> static -> dos` workflows
- PBS Pro and SLURM job-script generation from one JSON configuration
- Safe propagation of `CONTCAR` to the next stage
- Extraction of total energy, electronic convergence, and force information
- A computational hydrogen electrode helper for \(\Delta G_{H^*}\)
- Unit tests and GitHub Actions continuous integration

## Quick start

```bash
python -m vaspflow generate examples/si_bulk/workflow.json --output runs/si_bulk
python -m vaspflow status runs/si_bulk
python -m vaspflow collect runs/si_bulk --csv results.csv
python -m vaspflow her --clean -100.000 --adsorbed -103.450 --h2 -6.800 \
  --zpe-correction 0.04 --entropy-correction 0.20
```

The generator deliberately does not copy a `POTCAR`. Create it on the target
cluster using your institution's licensed pseudopotential installation.

## Repository layout

```text
vaspflow/               Python package and CLI
templates/              PBS Pro and SLURM script templates
examples/si_bulk/       Public toy workflow
tests/                   Parser and thermochemistry tests
```

## Configuration

Edit `examples/si_bulk/workflow.json` to set the scheduler, allocation, module,
executable, resources, and calculation stages. Machine-specific values are kept
outside the code, which makes the same workflow portable between clusters.

## Scientific notes

For adsorption thermochemistry, the helper implements

\[
\Delta G_{H^*} = G_{slab+H} - G_{slab} - \frac{1}{2}G_{H_2}
\]

where optional zero-point-energy and entropy corrections are supplied explicitly.
It does not assume that slab and gas-phase vibrational treatments are identical.

## License

MIT.

