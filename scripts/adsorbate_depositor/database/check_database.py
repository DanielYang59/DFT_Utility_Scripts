#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import yaml
from pathlib import Path
import argparse

def read_yaml_file(file_path):
    """
    Reads a YAML file and returns the parsed data.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return yaml.safe_load(file)
    except yaml.YAMLError as exc:
        print(f"Failed to read {file_path}.")
        if hasattr(exc, "problem_mark"):
            mark = exc.problem_mark
            print(f"Error position: (Line:{mark.line+1}, Column:{mark.column+1})")
        return None

def check_database(header_filename="pathway_database_header.yaml"):
    """
    Checks the integrity and structure of the adsorbate database.
    """
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
                    # Add your validation logic here.
                    # If validation passes:
                    passed.append(str(header_file))
                    # If validation fails:
                    # failed.append(str(header_file))
                else:
                    failed.append(str(header_file) + " could not be read.")
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
