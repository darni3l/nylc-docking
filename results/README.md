## Results

**Monomer docking:** top-scoring pose −5.496 kcal/mol (mode 1), 9 modes within a 4 kcal/mol window. Modes 2–3 cluster near mode 1 (~1.7–2.0 Å RMSD); modes 4–8 diverge substantially (up to 6+ Å RMSD), consistent with the ligand's high conformational flexibility (13 rotatable bonds). Replicate runs (5 seeds): mean −5.338 ± 0.183 kcal/mol.

![Monomer mode 1 — closeup of ligand at Thr-267]
(results/figures/mono/mode1_closeup.png)
*Monomer, mode 1 (top-scoring pose): closeup of the ligand relative to Thr-267.*

**Tetramer docking:** top-scoring pose −5.735 kcal/mol (mode 1). Replicate runs (5 seeds): mean −5.907 ± 0.177 kcal/mol — a real, reproducible improvement over the monomer (non-overlapping ranges), at first glance suggesting the tetrameric context improves binding.

**Catalytic geometry (OG1–carbonyl carbon distance):**

| | Mode 1 | Mode 2 | Mode 3 |
|---|---|---|---|
| Monomer | 3.1 Å | 4.3 Å | 5.2 Å |
| Tetramer | 4.8 Å | 5.8 Å | 3.8 Å |

Score and geometry rank differently: the monomer's best-*scoring* pose (mode 1) also has the best catalytic geometry, but the tetramer's best-*scoring* pose (mode 1) does not — tetramer mode 3, despite ranking third by score, has the most reaction-plausible geometry.

![Tetramer mode 3 — closeup of ligand at Thr-267]
(results/figures/tetra/mode3tetra_closeup.png)
*Tetramer, mode 3 (best catalytic geometry, though only third-ranked by score): closeup of the ligand relative to Thr-267.*

This confirms that Vina's score alone cannot be used to select a reaction-competent pose; geometric inspection relative to Thr-267 is necessary in both conditions.
