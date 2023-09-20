#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from pathlib import Path
from ase import Atoms
from ase.io import read
from typing import List

class AdsorbateGenerator:

    def __init__(self, POSCAR_adsorbate,atom_indexes, generate_rotations = False) -> None:
        # Check args
        if not POSCAR_adsorbate.is_file():
            raise FileNotFoundError(f"Adsorbate POSCAR file {POSCAR_adsorbate} not found.")
        if not isinstance(generate_rotations, bool):
            raise TypeError("Illegal datatype for \"generate_rotations\"")

        if len(atom_indexes) != len(set(atom_indexes)):
            raise ValueError("Duplicate found in adsorbate atom selection.")
        if len(atom_indexes) == 0:
            raise ValueError("Adsorbate atom selection is empty.")
        for index in atom_indexes:
            if index not in range(1, len(read(POSCAR_adsorbate, format="vasp")) + 1):
                raise ValueError(f"Illegal adsorbate index \"{index}\" (indexing starts from 1).")

        self.poscar = read(self.poscar_substrate, format="vasp")
        self.atom_indexes = atom_indexes
        self.generate_rotations = generate_rotations

    def _extract_atoms(self) -> Atoms:
        """
        Extracts specified atoms from a POSCAR file.

        Args:
            poscar_path (Path): Path to the POSCAR file.
            index_list (List[int]): List of atom indexes to extract (1-based indexing).

        Returns:
            Atoms: ASE Atoms object containing the extracted atoms.
        """
        # Correct index list (ASE uses 0-based indexing, while user provided 1-based indexing)
        corrected_index_list = [index - 1 for index in self.poscar]

        # Extract specified atoms
        return self.poscar[corrected_index_list]

    def _generate_rotations(self, ):
        #NOTE: warning and skip if only one atom
        pass


    def generate(self, work_mode="POSCAR"):
        assert work_mode in {"POSCAR", "DATABASE"}


# Test area
if __name__ == "__main__":
    adsorbate_generator = AdsorbateGenerator(
        POSCAR_adsorbate="",
        generate_rotations=True)

    adsorbates = adsorbate_generator.generate()
