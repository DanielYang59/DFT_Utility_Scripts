#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pathlib import Path
from copy import deepcopy
import warnings
from ase import Atoms
from ase.io import read
from typing import List, Dict

from .parse_adsorbate_database import parse_adsorbate_database

class AdsorbateGenerator:
    """
    Handles the generation of adsorbates based on various input types.

    Attributes:
        work_mode (str): Working mode ("POSCAR" or "DATABASE").
        path (Path): The path to the adsorbate POSCAR ("POSCAR" mode) or database directory ("DATABASE" mode).
        generate_rotations (bool): Whether to generate rotated versions.
        adsorbate_header_dict (Dict): The loaded adsorbate database dictionary for selected pathway.

    Methods:
        __init__ : Initialize the class.
        _extract_atoms : Extract specified atoms from a POSCAR file.
        _generate_rotations : Generate rotated versions of an adsorbate.
        _generate_rotated_adsorbate_dict : Generate dictionary of rotated adsorbates.
        _load_adsorbate_from_database_header : Load adsorbates based on a database header.
        generate_adsorbate_references : Generate adsorbate reference points.
        generate_adsorbates : Generate adsorbates based on the working mode.
    """

    def __init__(self, work_mode: str, path: Path, pathway_name: str = None, generate_rotations: bool = False) -> None:
        """
        Initialize the AdsorbateGenerator object.

        Args:
            work_mode (str): The working mode ("POSCAR" or "DATABASE").
            path (Path): Path to POSCAR file or database directory.
            pathway_name (str): Requested pathway name from database (only for "DATABASE" mode).
            generate_rotations (bool): Flag to generate rotated versions of adsorbate. Default is False.

        Raises:
            RuntimeError: If an illegal working mode is passed.
            FileNotFoundError: If the database directory does not exist.
            TypeError: If generate_rotations is not a boolean.
        """
        # Check work mode and corresponding path
        if work_mode == "POSCAR":
            if not path.is_file():
                raise FileNotFoundError("Adsorbate POSCAR not existing.")
        elif work_mode == "DATABASE":
            if not path.is_dir():
                raise FileNotFoundError("Adsorbate database not existing.")
        else:
            raise RuntimeError(f"Illegal working mode {work_mode} for adsorbate generator.")

        # Check boolean arg type
        if not isinstance(generate_rotations, bool):
            raise TypeError("Illegal datatype for \"generate_rotations\".")

        # Parse attributes
        self.work_mode = work_mode
        self.path = path
        self.generate_rotations = generate_rotations

        # Parse adsorbate database
        if work_mode == "DATABASE":
            self.adsorbate_header_dict = parse_adsorbate_database(path, pathway_name)
        else:
            self.adsorbate_header_dict = None

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

    def _load_adsorbate_from_database_header(self) -> Dict:
        """
        Load adsorbate from POSCARs based on database pathway header dict.

        Returns:
            Dict: A dictionary of loaded adsorbate POSCARs.

        Raises:
            ValueError: If required keys are missing from the database header or if indexing is not continuous.
        """
        adsorbate_POSCARs = {}

        for i, (step_key, step_info) in enumerate(self.adsorbate_header_dict.items(), start=1):
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
                path=self.database_path / POSCAR_path,
                atom_indexes=adsorbate_atoms
            )

        return adsorbate_POSCARs

    def generate_adsorbates(self, atom_indexes: List[int] = None) -> Dict[str, Atoms]:
        """
        Generate adsorbates based on the working mode.

        Args:
            atom_indexes (List[int]): Atom indexes to extract (only required for "POSCAR" mode).

        Returns:
            Dict[str, Atoms]: Dictionary of generated adsorbates, where keys are adsorbate names and values are Atoms objects.
        """
        if self.work_mode == "POSCAR":
            adsorbate_POSCARs = {"adsorbate": self._extract_atoms(self.path, atom_indexes)}

        else:
            adsorbate_POSCARs = self._load_adsorbate_from_database_header(database_path=self.path, pathway_header_dict=self.adsorbate_header_dict)

        # Generate rotations if required
        if self.generate_rotations:
            return self._generate_rotated_adsorbate_dict(self.adsorbate_header_dict)

        else:
            return adsorbate_POSCARs

    def _validate_poscar_ads_ref(self, poscar_ads_ref: List[int]) -> None:
        """Validates the poscar_ads_ref list."""
        if not isinstance(poscar_ads_ref, list) or not all(isinstance(x, int) for x in poscar_ads_ref):
            raise TypeError("poscar_ads_ref should be a list of integers.")

        if any(x < 1 for x in poscar_ads_ref):
            raise ValueError("All integers in poscar_ads_ref should be greater or equal to 1.")

        if len(poscar_ads_ref) != len(set(poscar_ads_ref)):
            raise ValueError("No duplicates are allowed in poscar_ads_ref.")

    def generate_adsorbate_references(self, adsorbates_dict: dict, poscar_ads_ref: List[int]) -> Dict[str, List[int]]:
        """
        Generate adsorbate reference points from adsorbates dict, based on adsorbate names.

        Args:
            adsorbates_dict (dict): The pre-generated adsorbate dict.
            poscar_ads_ref (list): The adsorbate reference list read from config, only needed for "POSCAR" mode.

        Returns:
            Dict[str, List[int]]: adsorbate reference atom index dict, the key is adsorbate name and the value being list of adsorbate atoms as reference.

        """
        # Check adsorbate dict datatype
        if not isinstance(adsorbates_dict, dict):
            raise TypeError("Wrong datatype for adsorbate dict is provided.")

        # Generate adsorbate reference points dict based on adsorbate names
        if self.work_mode == "POSCAR":
            self._validate_poscar_ads_ref(poscar_ads_ref)

            if len(adsorbates_dict) != 1:
                raise RuntimeError("Code work in POSCAR mode but adsorbate dict len is not 1.")

            return {list(adsorbates_dict.keys()[0]): poscar_ads_ref}

        else:  # "DATABASE" mode
            if poscar_ads_ref is not None:
                warnings.warn("Adsorbate reference set in config for DATABASE mode. Ignored.")

            reference_atoms_dict = {}

            for ads_name, ads_info in self.adsorbate_header_dict.items():
                reference_atoms = ads_info.get("reference_atoms")
                if reference_atoms is not None:
                    reference_atoms_dict[ads_name] = reference_atoms
                else:
                    raise ValueError(f"Reference atoms for {ads_name} is empty.")

            return reference_atoms_dict
