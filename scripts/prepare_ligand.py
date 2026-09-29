"""
prepare_ligand.py
Converts the PA2_opt ligand PDB into PDBQT format for AutoDock Vina,
using MGLTools' prepare_ligand4.py.
Cross-platform: paths resolved via paths_config.py and this script's own location.
"""

import os
import shutil
import subprocess
import paths_config

# --- Paths relative to this script's own location ---
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
RAW_DIR = os.path.join(SCRIPT_DIR, "..", "data", "raw")
PROCESSED_DIR = os.path.join(SCRIPT_DIR, "..", "data", "processed")

LIGAND_FILENAME = "PA2_opt.pdb"
OUTPUT_FILENAME = "PA2_opt.pdbqt"

FINAL_OUTPUT_PATH = os.path.join(PROCESSED_DIR, OUTPUT_FILENAME)

PREPARE_LIGAND_SCRIPT = os.path.join(paths_config.UTILITIES_DIR, "prepare_ligand4.py")

# Bare filenames here on purpose: prepare_ligand4.py internally chdir's
# to the output directory and re-reads the ligand by basename, so input
# and output must resolve in the SAME working directory (see cwd below).
cmd = [
    paths_config.MGLTOOLS_PYTHON,
    PREPARE_LIGAND_SCRIPT,
    "-l", LIGAND_FILENAME,
    "-o", OUTPUT_FILENAME,
    "-A", "hydrogens",
]

if __name__ == "__main__":
    print(f"Running on {paths_config.SYSTEM}")
    print("Command:", " ".join(cmd))
    print(f"Working directory: {RAW_DIR}")

    # Run with cwd=RAW_DIR so both the input read and MGLTools' internal
    # chdir-and-reread happen in the same folder as PA2_opt.pdb.
    result = subprocess.run(cmd, cwd=RAW_DIR, capture_output=True, text=True)

    print(result.stdout)
    if result.returncode != 0:
        print("ERROR:", result.stderr)
    else:
        # Output was written into RAW_DIR (since that was cwd) — move it
        # into data/processed/ where derived files belong.
        produced_path = os.path.join(RAW_DIR, OUTPUT_FILENAME)
        shutil.move(produced_path, FINAL_OUTPUT_PATH)
        print(f"Ligand PDBQT written to {FINAL_OUTPUT_PATH}")