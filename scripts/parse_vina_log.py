"""
parse_vina_log.py
Parses an AutoDock Vina output log into a clean CSV of mode/affinity/RMSD (both bounds).
Takes a run label so results from different runs (monomer, tetramer, ...) don't
overwrite each other.

Usage:
    python parse_vina_log.py monomer
    python parse_vina_log.py tetramer
"""

import re
import csv
import os
import sys

def vina_log_to_csv(log_file, csv_file):
    results = []

    with open(log_file, "r") as f:
        for line in f:
            match = re.match(
                r"\s*(\d+)\s+(-?\d+(?:\.\d+)?)\s+(-?\d+(?:\.\d+)?)\s+(-?\d+(?:\.\d+)?)",
                line
            )

            if match:
                mode = int(match.group(1))
                affinity = float(match.group(2))
                rmsd_lb = float(match.group(3))
                rmsd_ub = float(match.group(4))

                results.append([mode, affinity, rmsd_lb, rmsd_ub])

    with open(csv_file, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Mode", "Affinity (kcal/mol)", "RMSD l.b.", "RMSD u.b."])
        writer.writerows(results)

    print(f"Saved {len(results)} results to {csv_file}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python parse_vina_log.py <label>   e.g. monomer | tetramer")
        sys.exit(1)

    label = sys.argv[1]

    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    RESULTS_DIR = os.path.join(SCRIPT_DIR, "..", "results", "tables")

    log_file = os.path.join(RESULTS_DIR, f"{label}_log.txt")
    csv_file = os.path.join(RESULTS_DIR, f"{label}_scores.csv")

    vina_log_to_csv(log_file, csv_file)