#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pathlib import Path
from ase.io import read
from ase import Atoms
from typing import Union

def read_poscar(file_path: Union[str, Path]) -> Atoms:
    """
    Read a POSCAR file and return an ASE Atoms object.

    Parameters:
    file_path (Path): Path to the POSCAR file

    Returns:
    ase.Atoms: ASE Atoms object containing the POSCAR information
    """
    # Convert the file_path to a Path object if it's a string
    if isinstance(file_path, str):
        file_path = Path(file_path)

    # Check if the file exists
    if not file_path.exists():
        raise FileNotFoundError(f"The file {file_path} does not exist.")

    return read(file_path, format="vasp")
