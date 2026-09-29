"""
run_docking.py
Runs AutoDock Vina docking using a run-specific config file, then parses
the resulting log into a clean CSV. Takes a run label so files from
different runs (monomer, tetramer, ...) don't overwrite each other.

Usage:
    python run_docking.py monomer
    python run_docking.py tetramer
"""

import os
import subprocess
import sys
import paths_config

if len(sys.argv) != 2:
    print("Usage: python run_docking.py <label>   e.g. monomer | tetramer")
    sys.exit(1)

LABEL = sys.argv[1]

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_DIR = os.path.join(SCRIPT_DIR, "..", "config")
DATA_DIR = os.path.join(SCRIPT_DIR, "..", "data", "processed")
RESULTS_DIR = os.path.join(SCRIPT_DIR, "..", "results", "tables")

CONFIG_FILE = os.path.abspath(os.path.join(CONFIG_DIR, f"{LABEL}_vina_config.txt"))
OUT_FILENAME = f"{LABEL}_out.pdbqt"
LOG_FILE = os.path.join(RESULTS_DIR, f"{LABEL}_log.txt")
PARSE_SCRIPT = os.path.join(SCRIPT_DIR, "parse_vina_log.py")

cmd = [
    paths_config.VINA_EXE,
    "--config", CONFIG_FILE,
    "--out", OUT_FILENAME,  # bare filename: resolved via cwd=DATA_DIR below
    "--verbosity", "2",
]

if __name__ == "__main__":
    print(f"Running on {paths_config.SYSTEM}")
    print(f"Run label: {LABEL}")
    print("Command:", " ".join(cmd))
    print(f"Working directory: {DATA_DIR}")

    result = subprocess.run(cmd, cwd=DATA_DIR, capture_output=True, text=True)

    with open(LOG_FILE, "w") as f:
        f.write(result.stdout)

    if result.returncode != 0:
        print("ERROR:", result.stderr)
    else:
        print(f"Docking log written to {LOG_FILE}")

        print("Parsing log into CSV...")
        parse_result = subprocess.run(
            ["python", PARSE_SCRIPT, LABEL],
            capture_output=True, text=True
        )
        print(parse_result.stdout)
        if parse_result.returncode != 0:
            print("ERROR while parsing log:", parse_result.stderr)