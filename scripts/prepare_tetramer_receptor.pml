# prepare_tetramer_receptor.pml
# Cleans the raw 3AXG tetramer structure for receptor preparation:
# keeps only the four protein chains, strips solvent and free ions.
# Run with: pymol -cq scripts/prepare_tetramer_receptor.pml

load ../data/raw/3AXG.pdb, 3AXG_tetramer
remove not chain A+B+C+D
remove solvent
remove resn NA
save ../data/processed/3AXG_tetramer.pdb, 3AXG_tetramer