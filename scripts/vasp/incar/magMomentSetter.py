#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# TODO: need a default magmom dict somehow
default_magmom = {'Ti': 1.0, 'O': 0.0}

from pathlib import Path
from ase.io import read
from typing import Dict
import warnings

from src.vasp_incar import VaspIncar

def generate_magmom_tag(atom_dict: Dict[str, int], default_magmom_dict: Dict[str, float], default_magmom: float = 1.5) -> str:
    """
    Generate a magmom tag based on the provided atom dictionary and default magmom values.

    Parameters:
    - atom_dict (Dict[str, int]): A dictionary where keys are element symbols and values are the number of atoms.
    - default_magmom_dict (Dict[str, float]): A dictionary containing default magmom values for specific elements.
    - default_magmom (float, optional): The default magmom value to use for elements not found in default_magmom_dict.

    Returns:
    - str: The generated magmom tag formatted as "count*magmom element1 count*magmom element2 ...".

    If a specific element's magmom is not found in default_magmom_dict, a warning is issued, and the default_magmom value is used.

    """
    magmom_tag = ""

    for element, count in enumerate(atom_dict):
        if element in default_magmom_dict:
            magmom_tag += f"{count}*{default_magmom_dict[element]} "

        else:
            warnings.warn(f"Magmom for element {element} not found. Default value of {default_magmom} applied.")
            magmom_tag += f"{count}*{default_magmom} "

    return magmom_tag


def main():
    """
    Main function for updating the MAGMOM tag in the INCAR file based on atom counts from POSCAR.

    Reads atomic information from the POSCAR file, compiles the "MAGMOM" INCAR tag using the generate_magmom_tag function,
    updates the INCAR file with the new MAGMOM tag, and writes the modified INCAR file to a new file.

    The function assumes that the POSCAR and INCAR files are located in the current working directory.
    """
    # Read atom and counting from POSCAR
    atoms = read(Path.cwd() / "POSCAR")
    atom_dict = dict(zip(atoms.get_chemical_symbols(), atoms.get_atomic_numbers()))


    # Compile "MAGMOM" the INCAR tag
    magmom_tag = generate_magmom_tag(atom_dict, default_magmom)


    # Update INCAR
    incar_handler = VaspIncar(Path.cwd() / "INCAR")
    incar_handler.set_tag("MAGMOM", magmom_tag)
    incar_handler.write_out(Path.cwd() / "INCAR_new")


if __name__ == "__main__":
    main()
