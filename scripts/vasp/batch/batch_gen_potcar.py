#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from pathlib import Path

from ..general.is_vasp_dir import list_vasp_dirs

def call_generate_potcar(vasp_dir: Path, verbose: bool = True):
    """
    Call the generate_potcar.py script for the specified VASP directory.

    Parameters:
        vasp_dir (Path): The path to the VASP directory.
        verbose (bool): If True, print a message after generating POTCAR. Default is True.

    Note:
        This function changes the working directory to the specified VASP directory,
        executes the generate_potcar.py script, and then returns to the original working directory.

    """
    # Change to the VASP directory
    os.chdir(vasp_dir)

    # Call generate POTCAR function
    # TODO: a more pythonic method would be better
    generate_potcar_command = "python ../potcar/generate_potcar.py"
    os.system(generate_potcar_command)

    # Change back to the original working directory
    os.chdir("..")

    if verbose:
        print(f"POTCAR generated in {vasp_dir}.")

def main():
    # List VASP dirs under cwd
    vasp_dirs = list_vasp_dirs(Path.cwd())

    # Call generate_potcar script for each valid VASP directory
    for vasp_dir in vasp_dirs:
        call_generate_potcar(vasp_dir)

if __name__ == "__main__":
    main()
