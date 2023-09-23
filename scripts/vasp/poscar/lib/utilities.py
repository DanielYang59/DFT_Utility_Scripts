#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pathlib import Path
from ase.io import read, write
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

def find_or_request_poscar():
    """
    Search for a POSCAR file in the working directory and return its Path object.
    If none is found, prompt the user to input a path to POSCAR or CONTCAR manually.
    """
    working_dir = Path.cwd()

    # First, try to find a POSCAR file in the working directory
    filepath = working_dir / "POSCAR"
    if filepath.exists():
        return filepath

    # If not found, ask the user to input the path manually
    user_input = input("No POSCAR file found in the working directory. Please specify the path: ")
    user_path = Path(user_input)

    if user_path.exists():
        return user_path
    else:
        raise FileNotFoundError(f"The file at {user_path} does not exist.")
