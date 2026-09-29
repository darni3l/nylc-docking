"""
run_replicates.py
Runs multiple AutoDock Vina replicate docking runs (different random seeds)
for a given system label, parses each into its own CSV, and summarizes the
top-pose (mode 1) affinity across replicates as mean ± SD.

Usage:
    python run_replicates.py monomer 1 2 3 4 5
    python run_replicates.py tetramer 1 2 3 4 5
"""

import os
import subprocess
import sys
import csv
import statistics
import paths_config

if len(sys.argv) < 3:
    print("Usage: python run_replicates.py <label> <seed1> [seed2 ...]")
    sys.exit(1)

LABEL = sys.argv[1]
SEEDS = [int(s) for s in sys.argv[2:]]

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_DIR = os.path.join(SCRIPT_DIR, "..", "config")
DATA_DIR = os.path.join(SCRIPT_DIR, "..", "data", "processed")
RESULTS_DIR = os.path.join(SCRIPT_DIR, "..", "results", "tables")
PARSE_SCRIPT = os.path.join(SCRIPT_DIR, "parse_vina_log.py")

CONFIG_FILE = os.path.abspath(os.path.join(CONFIG_DIR, f"{LABEL}_vina_config.txt"))

if __name__ == "__main__":
    top_pose_affinities = []

    for seed in SEEDS:
        run_label = f"{LABEL}_seed{seed}"
        out_filename = f"{run_label}_out.pdbqt"
        log_file = os.path.join(RESULTS_DIR, f"{run_label}_log.txt")
        csv_file = os.path.join(RESULTS_DIR, f"{run_label}_scores.csv")

        cmd = [
            paths_config.VINA_EXE,
            "--config", CONFIG_FILE,
            "--out", out_filename,
            "--seed", str(seed),
            "--verbosity", "2",
        ]

        print(f"\n--- {LABEL}, seed {seed} ---")
        result = subprocess.run(cmd, cwd=DATA_DIR, capture_output=True, text=True)

        with open(log_file, "w") as f:
            f.write(result.stdout)

        if result.returncode != 0:
            print("ERROR:", result.stderr)
            continue

        parse_result = subprocess.run(
            ["python", PARSE_SCRIPT, run_label],
            capture_output=True, text=True
        )
        print(parse_result.stdout)
        if parse_result.returncode != 0:
            print("ERROR while parsing log:", parse_result.stderr)
            continue

        with open(csv_file, "r") as f:
            for row in csv.DictReader(f):
                if int(row["Mode"]) == 1:
                    top_pose_affinities.append(float(row["Affinity (kcal/mol)"]))
                    break

    if top_pose_affinities:
        mean_affinity = statistics.mean(top_pose_affinities)
        sd_affinity = statistics.stdev(top_pose_affinities) if len(top_pose_affinities) > 1 else 0.0

        summary_file = os.path.join(RESULTS_DIR, f"{LABEL}_replicate_summary.csv")
        with open(summary_file, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Seed", "Mode 1 Affinity (kcal/mol)"])
            for seed, aff in zip(SEEDS, top_pose_affinities):
                writer.writerow([seed, aff])
            writer.writerow([])
            writer.writerow(["Mean", mean_affinity])
            writer.writerow(["SD", sd_affinity])

        print(f"\n{LABEL}: mean = {mean_affinity:.3f} kcal/mol, SD = {sd_affinity:.3f}")
        print(f"Summary written to {summary_file}")
    else:
        print("No successful replicate runs to summarize.")