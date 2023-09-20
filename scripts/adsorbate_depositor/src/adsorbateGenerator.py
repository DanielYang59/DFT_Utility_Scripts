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

    def __init__(self, POSCAR_adsorbate: Path, atom_indexes: List[int], generate_rotations: bool = False) -> None:
        """
        Initialize the AdsorbateGenerator object.

        Args:
            POSCAR_adsorbate (Path): The path to the adsorbate POSCAR file.
            atom_indexes (List[int]): List of atom indexes to extract (1-based indexing).
            generate_rotations (bool): Flag to generate rotated versions of adsorbate. Default is False.

        Raises:
            FileNotFoundError: If the POSCAR file is not found.
            TypeError: If generate_rotations is not a boolean.
            ValueError: If atom_indexes contains duplicate or illegal indexes.
        """
        # Check args
        if not POSCAR_adsorbate.is_file():
            raise FileNotFoundError(f"Adsorbate POSCAR file {POSCAR_adsorbate} not found.")
        if not isinstance(generate_rotations, bool):
            raise TypeError("Illegal datatype for \"generate_rotations\"")

        if len(atom_indexes) != len(set(atom_indexes)):
            raise ValueError("Duplicate found in adsorbate atom selection.")
        if not atom_indexes:
            raise ValueError("Adsorbate atom selection is empty.")
        for index in atom_indexes:
            if index not in range(1, len(read(POSCAR_adsorbate, format="vasp")) + 1):
                raise ValueError(f"Illegal adsorbate index \"{index}\" (indexing starts from 1).")

        if not POSCAR_adsorbate.is_file():
            raise FileNotFoundError(f"Adsorbate POSCAR file {POSCAR_adsorbate} not found.")

        if not isinstance(generate_rotations, bool):
            raise TypeError("Illegal datatype for \"generate_rotations\".")

        if len(atom_indexes) != len(set(atom_indexes)):
            raise ValueError("Duplicate found in adsorbate atom selection.")

        if len(atom_indexes) == 0:
            raise ValueError("Adsorbate atom selection is empty.")

        for index in atom_indexes:
            if index not in range(1, len(read(POSCAR_adsorbate, format="vasp")) + 1):
                raise ValueError(f"Illegal adsorbate index \"{index}\" (indexing starts from 1).")

        self.poscar = read(POSCAR_adsorbate, format="vasp")
        self.atom_indexes = atom_indexes
        self.generate_rotations = generate_rotations

    def _extract_atoms(self) -> Atoms:
        """
        Extracts specified atoms from a POSCAR file.

        Returns:
            Atoms: ASE Atoms object containing the extracted adsorbate atoms.
        """
        # Correct index list (ASE uses 0-based indexing, while user provided 1-based indexing)
        corrected_index_list = [index - 1 for index in self.poscar]

        # Extract specified atoms
        return self.poscar[corrected_index_list]

    def _generate_rotations(self, adsorbate_atoms):
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
            warnings.warn("Adsorbate containing only one atom, rotation skipped.")
            return [adsorbate_atoms, ]

        else:
            # Define rotations: (axis, angle)
            rotations = [
                ("x", 90),  # Rotate 90 degrees about x
                ("x", -90), # Rotate -90 degrees about x
                ("y", 90),  # Rotate 90 degrees about y
                ("y", -90), # Rotate -90 degrees about y
                ("z", 180)  # Rotate 180 degrees about z (opposite face)
            ]

            rotated_adsorbates = []
            for axis, angle in rotations:
                rotated_adsorbate = deepcopy(adsorbate_atoms)
                rotated_adsorbate.rotate(axis, angle)
                rotated_adsorbates.append(rotated_adsorbate)

            return rotated_adsorbates

    def generate(self, work_mode="POSCAR"):
        assert work_mode in {"POSCAR", "DATABASE"}


# Test area
if __name__ == "__main__":
    adsorbate_generator = AdsorbateGenerator(
        POSCAR_adsorbate="",
        generate_rotations=True)

    adsorbates = adsorbate_generator.generate()
