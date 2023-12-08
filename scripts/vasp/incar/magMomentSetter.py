#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pathlib import Path
from typing import Dict
from ase.io import read

def read_element_from_poscar(poscarfile: Path) -> Dict[str, int]:
    """
    Read chemical elements and their counts from a VASP POSCAR file.

    Parameters:
        - poscarfile (Path): The path to the POSCAR file.

    Returns:
        - element_counts (Dict[str, int]): A dictionary containing the counts of each chemical element.
        The keys are element symbols, and the values are the corresponding counts.

    Example:
        >>> poscar_path = Path("fe3pd-ordered(100).POSCAR")
        >>> element_counts = read_element_from_poscar(poscar_path)
        >>> print(element_counts)
        {'Fe': 81, 'Pd': 27}
    """
    atoms = read(poscarfile)

    # Extract the chemical symbols and counts
    symbols = atoms.get_chemical_symbols()

    return {symbol: symbols.count(symbol) for symbol in set(symbols)}

def write_magmom_to_incar(incarfile: Path) -> None:
    pass


def magnetic_moment_setter(incarfile: Path) -> None:
    # Read elements from POSCAR
    elements = read_element_from_poscar()

    # Parse magnetic moment based on elements


    # Write magnetic moment into INCAR
    write_magmom_to_incar(incarfile)

if __name__ == "__main__":
    magnetic_moment_setter()
