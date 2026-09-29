"""
prepare_receptor.py
Converts a receptor PDB into PDBQT format for AutoDock Vina, using
MGLTools' prepare_receptor4.py. Takes a run label (monomer/tetramer)
to select the correct input/output pair.

Usage:
    python prepare_receptor.py monomer
    python prepare_receptor.py tetramer
"""

import os
import subprocess
import sys
import paths_config

if len(sys.argv) != 2:
    print("Usage: python prepare_receptor.py <label>   e.g. monomer | tetramer")
    sys.exit(1)

LABEL = sys.argv[1]

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
RAW_DIR = os.path.join(SCRIPT_DIR, "..", "data", "raw")
PROCESSED_DIR = os.path.join(SCRIPT_DIR, "..", "data", "processed")

# Maps each run label to its receptor input (source structure) and
# output (PDBQT) filenames. Add new labels here if the pipeline grows.
RECEPTOR_INPUTS = {
    "monomer": os.path.join(PROCESSED_DIR, "3AXG_chainA.pdb"),   # chain-A extract (derived via PyMOL)
    "tetramer": os.path.join(PROCESSED_DIR, "3AXG_tetramer.pdb"), # full tetramer, solvents/ions/heteroatoms stripped via PyMOL
}
RECEPTOR_OUTPUTS = {
    "monomer": os.path.join(PROCESSED_DIR, "3AXG_chainA.pdbqt"),
    "tetramer": os.path.join(PROCESSED_DIR, "3AXG_tetramer.pdbqt"),
}

if LABEL not in RECEPTOR_INPUTS:
    print(f"Unknown label '{LABEL}'. Valid options: {list(RECEPTOR_INPUTS)}")
    sys.exit(1)

RECEPTOR_IN = RECEPTOR_INPUTS[LABEL]
RECEPTOR_OUT = RECEPTOR_OUTPUTS[LABEL]

PREPARE_RECEPTOR_SCRIPT = os.path.join(paths_config.UTILITIES_DIR, "prepare_receptor4.py")

cmd = [
    paths_config.MGLTOOLS_PYTHON,
    PREPARE_RECEPTOR_SCRIPT,
    "-r", RECEPTOR_IN,
    "-o", RECEPTOR_OUT,
    "-A", "hydrogens",
    "-U", "nphs_lps_waters",
]

if __name__ == "__main__":
    print(f"Running on {paths_config.SYSTEM}")
    print(f"Run label: {LABEL}")
    print("Command:", " ".join(cmd))
    result = subprocess.run(cmd, capture_output=True, text=True)

    print(result.stdout)
    if result.returncode != 0:
        print("ERROR:", result.stderr)
    else:
        print(f"Receptor PDBQT written to {RECEPTOR_OUT}")