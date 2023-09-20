#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pathlib import Path
from copy import deepcopy
import warnings
from ase import Atoms
from ase.io import read
from typing import List

class AdsorbateGenerator:
    """
    Class for generating various configurations of adsorbates on a substrate.
    """

    def __init__(self, generate_rotations: bool = False) -> None:
        """
        Initialize the AdsorbateGenerator object.

        Args:
            generate_rotations (bool): Flag to generate rotated versions of adsorbate. Default is False.

        Raises:
            TypeError: If generate_rotations is not a boolean.
        """
        if not isinstance(generate_rotations, bool):
            raise TypeError("Illegal datatype for \"generate_rotations\".")

        self.generate_rotations = generate_rotations

    def _extract_atoms(self, POSCAR_adsorbate: Path, atom_indexes: List[int]) -> Atoms:
        """
        Extracts specified atoms from the loaded POSCAR file.

        Args:
            POSCAR_adsorbate (Path): The path to the adsorbate POSCAR file.
            atom_indexes (List[int]): List of atom indexes to extract (1-based indexing).

        Raises:
            FileNotFoundError: If the POSCAR file is not found.
            ValueError: If atom_indexes contains duplicate or illegal indexes.

        Returns:
            Atoms: ASE Atoms object containing the extracted adsorbate atoms.
        """
        if not POSCAR_adsorbate.is_file():
            raise FileNotFoundError(f"Adsorbate POSCAR file {POSCAR_adsorbate} not found.")

        if len(atom_indexes) != len(set(atom_indexes)):
            raise ValueError("Duplicate found in adsorbate atom selection.")

        if not atom_indexes:
            raise ValueError("Adsorbate atom selection is empty.")

        # Import POSCAR
        poscar = read(POSCAR_adsorbate, format="vasp")
        for index in atom_indexes:
            if index not in range(1, len(poscar) + 1):
                raise ValueError(f"Illegal adsorbate index \"{index}\" (indexing starts from 1).")

        # Extract adsorbate atoms
        corrected_index_list = [index - 1 for index in atom_indexes]
        return poscar[corrected_index_list]

    def _generate_rotations(self, adsorbate_atoms: Atoms) -> List[Atoms]:
        """
        Generate rotated versions of the given adsorbate.

        Args:
            adsorbate_atoms (Atoms): The Atoms object to rotate.

        Returns:
            List[Atoms]: A list of rotated Atoms objects.
        """
        assert isinstance(adsorbate_atoms, Atoms)

        if not adsorbate_atoms:
            raise ValueError("Empty adsorbate fed into adsorbate rotation generator.")

        elif len(adsorbate_atoms) == 1:
            warnings.warn("Adsorbate containing only one atom; rotation skipped.")
            return [adsorbate_atoms, ]

        else:
            rotations = [
                ("x", 90),  # Rotate 90 degrees about x
                ("x", -90), # Rotate -90 degrees about x
                ("y", 90),  # Rotate 90 degrees about y
                ("y", -90), # Rotate -90 degrees about y
                ("z", 180), # Rotate 180 degrees about z
            ]

            rotated_adsorbates = []
            for axis, angle in rotations:
                rotated_adsorbate = deepcopy(adsorbate_atoms)
                rotated_adsorbate.rotate(axis, angle)
                rotated_adsorbates.append(rotated_adsorbate)

            return rotated_adsorbates

    def generate(self, work_mode: str = "POSCAR"):
        """
        Generate adsorbates based on the working mode.

        Args:
            work_mode (str): The working mode ("POSCAR" or "DATABASE").

        Raises:
            RuntimeError: If an illegal working mode is passed.
        """
        if work_mode == "POSCAR":
            pass  # TODO

        elif work_mode == "DATABASE":
            pass  # TODO

        else:
            raise RuntimeError(f"Illegal working mode {work_mode} for adsorbate generator.")

# Test area
if __name__ == "__main__":
    adsorbate_generator = AdsorbateGenerator(
        POSCAR_adsorbate=Path("path/to/your/POSCAR/file"),
        atom_indexes=[1, 2, 3],
        generate_rotations=True)
