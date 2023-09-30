#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
from pathlib import Path
import yaml

def read_yaml_file(file_path):
    """Reads a YAML file and returns the parsed data."""
    try:
        with file_path.open("r", encoding="utf-8") as file:
            return yaml.safe_load(file)
    except yaml.YAMLError as exc:
        print(f"Failed to read {file_path}.")
        if hasattr(exc, 'problem_mark'):
            mark = exc.problem_mark
            print(f"Error position: (Line:{mark.line+1}, Column:{mark.column+1})")
        return None

def check_database(header_filename="pathway_database_header.yaml"):
    """Checks the integrity and structure of the adsorbate database."""
    passed = []
    failed = []
    warnings = []

    working_dir = Path(".")
    for folder in working_dir.iterdir():
        if folder.is_dir():
            header_file = folder / header_filename
            if header_file.exists():
                data = read_yaml_file(header_file)
                if data:
                    # Validation logic starts here
                    for pathway, pathway_data in data.get("pathways", {}).items():
                        # Check if the indices are continuous integers starting from 1
                        steps = list(pathway_data.keys())[2:]  # Skip 'reference_DOI' and 'comment'
                        indices = [int(s.split('_')[-1]) for s in steps]
                        if indices != list(range(1, len(steps) + 1)):
                            failed.append(f"{pathway} in {header_file} has non-continuous step indexing.")
                            continue
                        # More validation logic here.
                        passed.append(str(header_file))
                    # Validation logic ends here
                else:
                    failed.append(f"Failed to read {header_file}.")
            else:
                failed.append(f"{folder} does not contain a {header_filename}.")

    print("=== Check Passed ===")
    for p in passed:
        print(f"{p} has passed all checks.")

    print("\n=== Check Failed ===")
    for f in failed:
        print(f)

    print("\n=== Warnings ===")
    for w in warnings:
        print(w)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Check the integrity of the adsorbate database.")
    parser.add_argument("--header", default="pathway_database_header.yaml", help="Name of the header file to check.")
    args = parser.parse_args()

    check_database(header_filename=args.header)
