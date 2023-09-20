#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pathlib import Path
from copy import deepcopy
import warnings
from ase import Atoms
from ase.io import read
from typing import List, Dict

from parse_adsorbate_database import parse_adsorbate_database

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
        adsorbate_poscar = poscar[corrected_index_list]
        if len(adsorbate_poscar) >= 10:
            warnings.warn("Large adsorbate requested (more than 10 atoms). Make sure this is intended.")
        return adsorbate_poscar

    def _generate_rotations(self, adsorbate_atoms: Atoms) -> List[Atoms]:
        """
        Generate rotated versions of the given adsorbate.

        Args:
            adsorbate_atoms (Atoms): The Atoms object to rotate.

        Returns:
            List[Atoms]: A list of rotated Atoms objects.
        """
        if not isinstance(adsorbate_atoms, Atoms):
            raise TypeError("Adsorbate fed into rotation generator should be ASE.Atoms.")

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

    def _generate_rotated_adsorbate_dict(self, adsorbate_dict: Dict[str, Atoms]) -> Dict[str, Atoms]:
        """
        Generate a new dictionary containing rotated versions of each original adsorbate.

        Args:
            adsorbate_dict (Dict[str, Atoms]): Original dictionary containing adsorbates.

        Returns:
            Dict[str, Atoms]: A new dictionary containing rotated versions of each original adsorbate.
        """

        rotated_adsorbate_dict = {}

        for name, atoms in adsorbate_dict.items():
            rotated_atoms_list = self._generate_rotations(atoms)
            for i, rotated_atoms in enumerate(rotated_atoms_list):
                new_name = f"{name}_rotation_{i}"
                rotated_adsorbate_dict[new_name] = rotated_atoms

        return rotated_adsorbate_dict

    def _load_adsorbate_from_database_header(self, database_path: Path, pathway_header_dict: Dict) -> Dict:
        """
        Load adsorbate from POSCARs based on database pathway header dict.

        Args:
            database_path (Path): The path to the adsorbate database directory.
            pathway_header_dict (Dict): The adsorbate database header dictionary.

        Returns:
            Dict: A dictionary of loaded adsorbate POSCARs.

        Raises:
            FileNotFoundError: If the database directory does not exist.
            TypeError: If the wrong data type is passed for the pathway_header_dict.
        """

        if not database_path.is_dir():
            raise FileNotFoundError("Adsorbate database not existing.")
        if not isinstance(pathway_header_dict, dict):
            raise TypeError("Wrong datatype for the adsorbate header dictionary.")

        adsorbate_POSCARs = {}

        for i, (step_key, step_info) in enumerate(pathway_header_dict.items(), start=1):
            if f"step_{i}" != step_key:
                raise ValueError(f"Step keys must be indexed continuously from 1. Found {step_key} instead.")

            name = step_info.get("name")
            if not name:
                raise ValueError(f"Missing 'name' for {step_key}.")

            POSCAR_path = step_info.get("POSCAR_path")
            if not POSCAR_path:
                raise ValueError(f"Missing 'POSCAR_path' for {step_key}.")

            adsorbate_atoms = step_info.get("adsorbate_atoms")
            if not adsorbate_atoms:
                raise ValueError(f"Missing 'adsorbate_atoms' for {step_key}.")

            adsorbate_POSCARs[name] = self._extract_atoms(
                path=database_path / POSCAR_path,
                atom_indexes=adsorbate_atoms
            )

        return adsorbate_POSCARs

    def generate(self, work_mode: str, path: Path, atom_indexes: List[int] = None, pathway_name: str = None):
        """
        Generate adsorbates based on the working mode.

        Args:
            work_mode (str): The working mode ("POSCAR" or "DATABASE").
            path (Path): The path to the adsorbate POSCAR file or DATABASE dir.
            atom_indexes (List[int]): List of atom indexes to extract from "POSCAR".
            pathway_name (str): name of requested pathway from "DATABASE".

        Raises:
            RuntimeError: If an illegal working mode is passed.
        """
        if work_mode not in {"POSCAR", "DATABASE"}:
            raise RuntimeError(f"Illegal working mode {work_mode} for adsorbate generator.")

        if work_mode == "POSCAR":
            adsorbate_POSCARs = {"adsorbate": self._extract_atoms(path, atom_indexes)}

        else:
            adsorbate_header_dict = parse_adsorbate_database(path, pathway_name, header="pathway_database_header.yaml")

            adsorbate_POSCARs = self._load_adsorbate_from_database_header(database_path=path, pathway_header_dict=adsorbate_header_dict)

        # Generate rotations if required
        if self.generate_rotations:
            return self._generate_rotated_adsorbate_dict(adsorbate_header_dict)

        else:
            return adsorbate_POSCARs
