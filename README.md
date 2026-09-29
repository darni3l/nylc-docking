# NylC–Polyamide Docking Pipeline

Molecular docking pipeline studying how a nylon-oligomer hydrolase (NylC) binds a polyamide dimer substrate, comparing monomeric and tetrameric receptor context, as a precursor step to molecular dynamics simulation of the catalytic mechanism.

## Background

This docking project is conducted in the context of a collaboration with Dr. Dirk Wacker (Polysecure GmbH), with the objective of studying and applying the nylonase catalytic activity of a biomolecule (NylC) toward the depolymerization of polyamides. The goal is twofold: (1) identify the best docking poses as a foundation for subsequent molecular dynamics simulations, and (2) assess whether docking into the enzyme's native tetrameric assembly changes binding outcomes compared to the isolated monomer.

NylC is a known enzyme of the nylonase family, recognized for promising enzymatic properties in polymer degradation (Sun et al., 2025). Polyamides, meanwhile, are an abundant class of plastic polymers whose recycling remains problematic (Bourgery et al., 2026). Depolymerizing these plastics into their reusable monomeric form is therefore of significant interest for sustainable plastics recycling.

This repository contains a full docking pipeline for a dimeric polyamide ligand (PA2_opt) against (1) the monomeric form of NylC (chain A) and (2) its native tetrameric assembly, with particular focus on the catalytic residue Thr-267 (Negoro et al., 2012).

**Structure used:** PDB [3AXG](https://www.rcsb.org/structure/3AXG) — NylC from *Agromyces* sp. strain KY5R.

## Repository contents
```
nylc-docking/
├── data/
│ ├── raw/ # Original, unmodified inputs: 3AXG.pdb, FASTA, PA2_opt.pdb
│ └── processed/ # Derived files: chain-A extract, cleaned tetramer, PDBQT conversions
├── scripts/ # Full pipeline: structure prep → docking → results parsing → replicates
├── config/ # Vina parameters per run (monomer_vina_config.txt, tetramer_vina_config.txt)
├── results/
│ ├── tables/ # Parsed scores, catalytic distances, replicate summaries (CSV)
│ ├── figures/ # Pose visualizations, split into mono/ and tetra/ subfolders
│ └── docked_poses/ # Output docked structures (PDBQT)
└── docs/ # Extended methods notes
```

## Methods (summary)

The pipeline: (1) prepares each receptor — chain A extracted via PyMOL for the monomer run, or the full tetramer with solvent/ions stripped via PyMOL for the tetramer run — and converts both to PDBQT via MGLTools; (2) prepares the PA2_opt ligand PDBQT via MGLTools; (3) runs AutoDock Vina 1.2.7 with a grid box centered on Thr-267, separately configured for each receptor; (4) parses raw Vina output into tabulated results; (5) repeats each run across 5 seeds to assess score reproducibility.

Full methodological detail — including grid box rationale, the tetramer's inter-chain distance analysis, and known tool-specific quirks encountered during setup — is documented in [`docs/methods.md`](docs/methods.md).

## Setup

### Prerequisites (external tools — not pip-installable)

- [AutoDock Vina 1.2.7](https://vina.scripps.edu/)
- [MGLTools 1.5.7](https://ccsb.scripps.edu/mgltools/)
- [PyMOL](https://pymol.org/)
- Python 3.10+ (standard library only — see `requirements.txt`)

### Configuration

Before running any script, edit `scripts/paths_config.py` to match your local install locations for MGLTools and Vina. This is the only file that needs machine-specific changes.

> **Note:** Windows install paths have been tested directly. macOS/Linux paths in `paths_config.py` are typical defaults and have not been verified on those platforms — adjust as needed.

### Running the pipeline

```bash
python scripts/prepare_receptor.py monomer
python scripts/prepare_receptor.py tetramer
python scripts/prepare_ligand.py
python scripts/run_docking.py monomer
python scripts/run_docking.py tetramer
```

Each `run_docking.py` call runs Vina and automatically parses the resulting log into `results/tables/{label}_scores.csv`.

To reproduce the replicate reproducibility analysis:
```bash
python scripts/run_replicates.py monomer 1 2 3 4 5
python scripts/run_replicates.py tetramer 1 2 3 4 5
```

## Results

**Monomer docking:** top-scoring pose −5.496 kcal/mol (mode 1), 9 modes within a 4 kcal/mol window. Modes 2–3 cluster near mode 1 (~1.7–2.0 Å RMSD); modes 4–8 diverge substantially (up to 6+ Å RMSD), consistent with the ligand's high conformational flexibility (13 rotatable bonds). Replicate runs (5 seeds): mean −5.338 ± 0.183 kcal/mol.

**Tetramer docking:** top-scoring pose −5.735 kcal/mol (mode 1). Replicate runs (5 seeds): mean −5.907 ± 0.177 kcal/mol — a real, reproducible improvement over the monomer (non-overlapping ranges), at first glance suggesting the tetrameric context improves binding.

**Catalytic geometry (OG1–carbonyl carbon distance):**

| | Mode 1 | Mode 2 | Mode 3 |
|---|---|---|---|
| Monomer | 3.1 Å | 4.3 Å | 5.2 Å |
| Tetramer | 4.8 Å | 5.8 Å | 3.8 Å |

Score and geometry rank differently: the monomer's best-*scoring* pose (mode 1) also has the best catalytic geometry, but the tetramer's best-*scoring* pose (mode 1) does not — tetramer mode 3, despite ranking third by score, has the most reaction-plausible geometry. This confirms that Vina's score alone cannot be used to select a reaction-competent pose; geometric inspection relative to Thr-267 is necessary in both conditions.

**Why does the tetramer score better?** Widening the residue shell around chain A's Thr-267 to 6–8 Å found no contribution from chains B/C/D — the immediate active-site pocket is structurally unaffected by the other three chains. Investigating further, 34 atoms from chains B/C/D were found lying within 13 Å of chain A's Thr-267 OG1 — inside the 25 Å search box used for docking, despite being well outside any real interaction distance. This indicates the monomer/tetramer score gap is a **search-box inclusion artifact** (extra atoms present in the grid box subtly reshaping the search landscape), not a genuine mechanistic effect of oligomerization on the active site itself.

Full results tables are in [`results/tables/`](results/tables/); pose visualizations are in [`results/figures/mono/`](results/figures/mono/) and [`results/figures/tetra/`](results/figures/tetra/).

## Limitations & next steps

- **Rigid receptor docking:** NylC is treated as rigid throughout; real active sites have side-chain (and sometimes backbone) flexibility that rigid docking cannot capture. A simplification to revisit with flexible-residue docking or MD.
- **Scoring vs. reaction-competent geometry:** Vina's scoring function has no concept of catalytic geometry, confirmed directly by this project's own results (see above) — top-scoring poses were visually inspected for proximity/angle of the ligand's hydrolyzable amide bond relative to Thr-267 OG1, since score alone cannot identify reaction-competent poses.
- **Search-box composition affects scoring:** the tetramer's improved score was traced to atoms incidental to the search box rather than genuine active-site contacts — a reminder that grid box design should be scrutinized whenever comparing receptor conditions with different overall geometry.
- **Next:** MD simulation of the top reaction-plausible candidate(s) — monomer mode 1 and tetramer mode 3 — to assess pose stability and refine catalytic geometry beyond what rigid docking can show.

## License & citation

This project is licensed under the [MIT License](LICENSE).

If referencing this work, please cite: https://github.com/darni3l/nylc-docking
