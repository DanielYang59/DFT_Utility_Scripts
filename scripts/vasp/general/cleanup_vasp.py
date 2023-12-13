#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# TODO: this script is not tested

from pathlib import Path
import shutil

def clean_vasp_files(directory: Path, job_script: str = "script.sh", verbose: bool = True):
    """
    Cleans up VASP output files, keeping only the essential ones.
    Moves other specified VASP output files to a backup directory,
    generating a new backup directory if needed.

    Args:
        directory (Path): The directory containing VASP files.
        job_script (str): The name of the job submit script.
        verbose (bool): verbosity. Defaults to True.
    """
    # Define essential and unnecessary files
    essential_files = ["INCAR", "POSCAR", "POTCAR", "KPOINTS", job_script]

    files_to_remove = [
        "OUTCAR", "OSZICAR", "WAVECAR", "CHGCAR", "EIGENVAL", "vasprun.xml",
        "XDATCAR", "CONTCAR", "IBZKPT", "DOSCAR", "PCDAT", "REPORT"
    ]

    # Create a new backup directory
    backup_index = 1
    while True:
        backup_dir = directory / f"vasp_backup_{backup_index}"
        if not backup_dir.exists():
            backup_dir.mkdir()
            break
        backup_index += 1

    # Move VASP output files to the backup directory
    for file_path in directory.iterdir():
        if file_path.is_file():
            if file_path.name in files_to_remove:
                file_path.unlink(missing_ok=True)  # Remove unnecessary VASP output files

            elif file_path.name in essential_files:
                shutil.copy2(file_path, backup_dir / file_path.name)  # Copy essential files to the backup directory

            else:
                pass  # ignore other files

    # Verbose
    if verbose:
        print(f"VASP dir {directory} cleaned up.")

if __name__ == "__main__":
    # Clean up current working directory for VASP
    clean_vasp_files(Path.cwd())
