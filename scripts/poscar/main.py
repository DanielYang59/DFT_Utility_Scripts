#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
from pathlib import Path

from src.utilities import find_or_request_poscar, discover_functions
from src.fix_atoms import fix_atoms
from src.remove_atoms import remove_atoms
from src.replace_atoms import replace_atoms
from src.adjust_vacuum import adjust_vacuum
# from src.coordinate_system_transfer import X

def main(file_path):
    """
    Main function for manipulating POSCAR files.
    """
    pass  # TODO:

if __name__ == "__main__":
    # Initialize argument parser
    parser = argparse.ArgumentParser(description="Manipulate POSCAR files.")
    parser.add_argument("-f", "--file_path", type=str, help="Path to the POSCAR file.", default=None)

    # Parse command-line arguments
    args = parser.parse_args()

    try:
        # Use utility function to get the POSCAR file path
        if args.file_path:
            file_path = find_or_request_poscar(Path(args.file_path))
        else:
            file_path = find_or_request_poscar()

        # If a valid file path is obtained, run the main function
        if file_path and file_path.exists():
            main(file_path)
        else:
            print("No valid POSCAR or CONTCAR file found. Exiting.")

    except FileNotFoundError as e:
        print(e)

    # List of modules to discover functions from
    modules = [fix_atoms, remove_atoms, replace_atoms, adjust_vacuum]  # Add more modules as needed

    # Discover available functions
    discover_functions(modules)
