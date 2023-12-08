#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pathlib import Path
from ase.io import read
from ase.io.vasp import write_incar
from typing import Dict

class MagneticMomentUpdater:
    def __init__(self, poscarfile: Path = Path.cwd() / "POSCAR", incarfile: Path = Path.cwd() / "INCAR"):
        self.poscarfile = poscarfile
        self.incarfile = incarfile

    def reset_magnetic_moment(self, magmom_dict: Dict[str, float]) -> None:
        """
        Reset magnetic moments in the INCAR file based on a predefined magmom dictionary.

        Parameters:
            - magmom_dict (Dict[str, float]): A dictionary containing the magnetic moments for each element.
              Keys are element symbols, and values are the corresponding magnetic moments.
        """
        # Write magnetic moment into INCAR
        self._write_magmom_to_incar(magmom_dict)

    def _write_magmom_to_incar(self, magmom_dict: Dict[str, float]) -> None:
        """
        Write magnetic moments to a VASP INCAR file using ASE.

        Parameters:
            - magmom_dict (Dict[str, float]): A dictionary containing the magnetic moments for each element.
              Keys are element symbols, and values are the corresponding magnetic moments.
        """
        atoms = read(self.incarfile)

        # Set initial magnetic moments
        for symbol, magmom in magmom_dict.items():
            atoms.set_initial_magnetic_moments(symbols=symbol, magmoms=magmom)

        # Write INCAR file
        write_incar(self.incarfile / "_new", atoms)

if __name__ == "__main__":
    updater = MagneticMomentUpdater()
    magmom_data = {'Fe': 2.0, 'Pd': -1.5}  # TODO:
    updater.reset_magnetic_moment(magmom_data)
