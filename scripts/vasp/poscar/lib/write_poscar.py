#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pathlib import Path
from ase.io import write
from ase import Atoms

def write_poscar(atoms: Atoms, file_path: str, overwrite: bool = False) -> None:
    """
    Write an ASE Atoms object to a POSCAR file.

    Parameters:
        atoms (ase.Atoms): The ASE Atoms object to write to the POSCAR file.
        file_path (Union[Path, str]): Path to the POSCAR file, can be either a string or a pathlib.Path object.
        overwrite (bool): Whether to overwrite the file if it already exists. Defaults to False.
    """
    # Convert the file_path to a Path object if it's a string
    if isinstance(file_path, str):
        file_path = Path(file_path)

    # Check if the file already exists
    if file_path.exists() and not overwrite:
        raise FileExistsError(f"The file {file_path} already exists. Use overwrite=True to overwrite it.")

    write(file_path, atoms, format="vasp")
