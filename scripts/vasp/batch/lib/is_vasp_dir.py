#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pathlib import Path
import warnings

def is_valid_vasp_dir(path: Path) -> bool:
    """
    Check if a directory contains essential VASP files.

    Args:
        path (Path): Path to the directory to be checked.

    Returns:
        bool: True if the directory contains all necessary VASP files, False otherwise.
    """
    # If path doesn't exist
    if not path.is_dir():
        warnings.warn(f"Dir {path} does not exist.")
        return False

    # If path exists
    else:
        vasp_core_files = ['INCAR', 'POSCAR', 'POTCAR', 'KPOINTS']

        for file in vasp_core_files:
            if not (path / file).is_file():
                print(f"VASP core file {file} missing in {path}.")
                return False

        return True
