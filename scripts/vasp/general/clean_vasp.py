#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# TODO: this script would need double check (why essential_files is unused)

import os
from pathlib import Path

def clean_vasp_files(directory: Path, job_script: str = "script.sh", verbose: str = "silent"):
    """
    Cleans up VASP output files, keeping only the essential ones.
    Moves other specified VASP output files to a backup directory,
    generating a new backup directory if needed.

    Args:
        directory (Path): The directory containing VASP files.
        job_script (str): The name of the job submit script.
        verbose (str): Level of verbosity ("silent", "verbose").
    """
    essential_files = ["INCAR", "POSCAR", "POTCAR", "KPOINTS", job_script]
    vasp_output_files = [
        "OUTCAR", "OSZICAR", "WAVECAR", "CHGCAR", "EIGENVAL", "vasprun.xml",
        "XDATCAR", "CONTCAR", "IBZKPT", "DOSCAR", "PCDAT", "REPORT"
    ]

    backup_index = 1

    while True:
        backup_dir = directory / f"output_backup_{backup_index}"
        if not backup_dir.exists():
            backup_dir.mkdir()
            break
        backup_index += 1

    for file_path in directory.iterdir():
        if file_path.is_file() and file_path.name in vasp_output_files:
            new_path = backup_dir / file_path.name
            file_path.rename(new_path)
            if verbose == "verbose":
                print(f"Moved {file_path.name} to {backup_dir}")

if __name__ == "__main__":
    current_directory = Path(os.getcwd())
    clean_vasp_files(current_directory)
