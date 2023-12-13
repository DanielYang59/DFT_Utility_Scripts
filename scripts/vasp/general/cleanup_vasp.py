#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# TODO: this script is not tested

from pathlib import Path
import shutil

def cleanup_vasp_files(directory: Path, job_script: str = "script.sh", verbose: bool = True):
    """
    Cleans up VASP output files, keeping only the essential ones.
    Moves other specified VASP output files to a backup directory,
    generating a new backup directory if needed.

    Args:
        directory (Path): The directory containing VASP files.
        job_script (str): The name of the job submit script.
        verbose (bool): Verbosity. Defaults to True.
    """
    # Define files to keep
    files_to_keep = ["INCAR", "POSCAR", "POTCAR", "KPOINTS", job_script]

    # Create a new backup directory
    backup_index = 1
    while True:
        backup_dir = directory / f"vasp_backup_{backup_index}"
        if not backup_dir.exists():
            backup_dir.mkdir()
            break
        backup_index += 1

    # Move other files to the backup directory
    for file_path in directory.iterdir():
        if file_path.name not in files_to_keep:
            shutil.move(file_path, backup_dir / file_path.name)

    # Verbose
    if verbose:
        print(f"VASP dir {directory} cleaned up.")

if __name__ == "__main__":
    # Clean up current working directory for VASP
    cleanup_vasp_files(Path.cwd())
