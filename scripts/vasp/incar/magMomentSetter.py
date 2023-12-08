#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pathlib import Path
from typing import Dict
from ase.io import read
from ase.io.vasp import write_incar

def read_element_from_poscar(poscarfile: Path) -> Dict[str, float]:
    """
    Read chemical elements and their counts from a VASP POSCAR file.

    Parameters:
        - poscarfile (Path): The path to the POSCAR file.

    Returns:
        - element_counts (Dict[str, float]): A dictionary containing the counts of each chemical element.
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

def write_magmom_to_incar(incarfile: Path, magmom_dict: Dict[str, int]) -> None:
    """
    Write magnetic moments to a VASP INCAR file.

    Parameters:
        - incarfile (Path): The path to the INCAR file.
        - magmom_dict (Dict[str, float]): A dictionary containing the magnetic moments for each element.
        Keys are element symbols, and values are the corresponding magnetic moments.

    Example:
        >>> incar_path = Path("INCAR")
        >>> magmom_data = {'Fe': 2.0, 'Pd': -1.5}
        >>> write_magmom_to_incar(incar_path, magmom_data)
    """
    atoms = read(incarfile)

    # Set initial magnetic moments
    for symbol, magmom in magmom_dict.items():
        atoms.set_initial_magnetic_moments(symbols=symbol, magmoms=magmom)

    # Write INCAR file
    write_incar(str(incarfile), atoms)

def magnetic_moment_setter(incarfile: Path) -> None:
    # Read elements from POSCAR
    elements = read_element_from_poscar()

    # Parse magnetic moment based on elements
    element_magmoms = None

    # Write magnetic moment into INCAR
    write_magmom_to_incar(incarfile, element_magmoms)

if __name__ == "__main__":
    magnetic_moment_setter()
