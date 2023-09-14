#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pathlib import Path
from ase.io import read, write
import inspect

def read_poscar(file_path):
    """
    Read a POSCAR file and return an ASE Atoms object.

    Parameters:
    file_path (Path): Path to the POSCAR file

    Returns:
    ase.Atoms: ASE Atoms object containing the POSCAR information
    """
    return read(file_path, format="vasp")

def write_poscar(atoms, filepath):
    """
    Write an ASE Atoms object to a POSCAR file.
    """
    write(filepath, atoms, format="vasp")

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

def discover_functions(module_list):
    """
    Discover available functions in a list of modules.
    """
    for module in module_list:
        functions = [o for o in inspect.getmembers(module) if inspect.isfunction(o[1])]
        for i, (name, _) in enumerate(functions):
            print(f"{module.__name__}: Function {i + 1}: {name}")
