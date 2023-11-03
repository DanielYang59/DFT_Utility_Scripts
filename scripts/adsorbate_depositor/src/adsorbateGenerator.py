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
        corrected_index_list = [index - 1 for index in atom_indexes]  # offset to 0-indexed (Atoms)
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
            raise TypeError(f"Adsorbate fed into rotation generator should be ASE.Atoms, got {type(adsorbate_atoms)}.")

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
            # Generate rotated Atoms
            rotated_atoms_list = self._generate_rotations(atoms)

            # Generate name names (for easy POSCAR output)
            for i, rotated_atoms in enumerate(rotated_atoms_list):
                new_name = f"{name}_rotation_{i}"
                rotated_adsorbate_dict[new_name] = rotated_atoms

        return rotated_adsorbate_dict

    def _load_adsorbate_from_database_header(self) -> Dict[str, Atoms]:
        """
        Load adsorbate from POSCARs based on database pathway header dict.

        Returns:
            Dict: A dictionary of loaded adsorbate POSCARs.

        Raises:
            ValueError: If required keys are missing from the database header or if indexing is not continuous.
        """
        # Check for illegal tags in adsorbate header dict
        for key in self.adsorbate_header_dict.keys():
            if key not in {"reference_DOI", "comment"} and not key.startswith("step_"):
                raise ValueError(f"Illegal key {key} found in adsorbate header.")

        # Check and parse "step_N" tags
        adsorbate_POSCARs = {}
        step_keys = [key for key in self.adsorbate_header_dict.keys() if key.startswith("step_")]

        for i, step_key in enumerate(step_keys, start=1):
            if f"step_{i}" != step_key:
                raise ValueError(f"Discontinuous reaction step {i} detected in adsorbate header.")
            else:
                name = self.adsorbate_header_dict[step_key]["name"]
                # Load POSCAR
                adsorbate_POSCARs[name] = self._extract_atoms(
                    POSCAR_adsorbate=self.path / self.adsorbate_header_dict[step_key]["POSCAR_path"],
                    atom_indexes=self.adsorbate_header_dict[step_key]["adsorbate_atoms"]
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
            adsorbate_POSCARs = self._load_adsorbate_from_database_header()

        # Generate rotations if required
        if self.generate_rotations:
            return self._generate_rotated_adsorbate_dict(adsorbate_POSCARs)

        else:
            return adsorbate_POSCARs

    def _validate_poscar_ads_ref(self, poscar_ads_ref: List[int]) -> None:
        """
        Validates the `poscar_ads_ref` list to ensure it meets the required specifications.

        Parameters:
            poscar_ads_ref (List[int]): A list of integers representing the reference indexes in a POSCAR file.

        Raises:
            TypeError: If `poscar_ads_ref` is not a list or contains non-integer elements.
            ValueError: If any integer in `poscar_ads_ref` is less than 1 or if duplicates are present.
        """
        if not isinstance(poscar_ads_ref, list) or not all(isinstance(x, int) for x in poscar_ads_ref):
            raise TypeError("poscar_ads_ref should be a list of integers.")

        if any(x < 1 for x in poscar_ads_ref):
            raise ValueError("All integers in poscar_ads_ref should be greater or equal to 1.")

        if len(poscar_ads_ref) != len(set(poscar_ads_ref)):
            raise ValueError("No duplicates are allowed in poscar_ads_ref.")

    def _regenerate_reference_indexing(self, adsorbate_atoms: List[int], reference_atoms: List[int])-> List[int]:
        """
        Validate and regenerate the reference atom indexing based on their order in the adsorbate atoms list.

        Args:
            adsorbate_atoms (List[int]): List of atom indexes for the adsorbate.
            reference_atoms (List[int]): List of atom indexes used as reference.

        Returns:
            List[int]: Regenerated list of reference atoms, representing their order in the adsorbate list starting from 0 (0-indexed).

        Raises:
            ValueError: If there are repeated elements in either of the atom lists.
            ValueError: If atom indexes are not integers starting from 1.
            ValueError: If reference atoms are not a subset of the adsorbate atoms.

        Note:
            DEBUG: Do the Atoms object indexings keep original order after "extraction"?
        """
        # Make sure there are no repeated elements in two args
        if len(set(adsorbate_atoms)) != len(adsorbate_atoms) or len(set(reference_atoms)) != len(reference_atoms):
            raise ValueError("There should be no repeated elements in the atom lists.")

        # Make sure every element is an integer starting from 1
        for atom in adsorbate_atoms + reference_atoms:
            if not isinstance(atom, int) or atom < 1:
                raise ValueError("All atom indexes must be integers starting from 1.")

        # Make sure reference atoms is a subset or equal of adsorbate atoms
        if not set(reference_atoms).issubset(set(adsorbate_atoms)):
            raise ValueError("Reference atoms must be a subset or equal to the adsorbate atoms.")

        # Regenerate reference atom indexing (0-indexed)
        return [adsorbate_atoms.index(atom) for atom in reference_atoms]

    def _load_adsorbate_ref_from_database_header(self) -> Dict[str, List[int]]:
        """
        Load adsorbate references based on database pathway header dict.

        Returns:
            Dict: A dictionary of loaded adsorbate references (0-indexed).

        Raises:
            ValueError: If required keys are missing from the database header or if indexing is not continuous.
        """
        # Check for illegal tags in adsorbate header dict
        for key in self.adsorbate_header_dict.keys():
            if key not in {"reference_DOI", "comment"} and not key.startswith("step_"):
                raise ValueError(f"Illegal key {key} found in adsorbate header.")

        # Check and parse "step_N" tags
        adsorbate_references = {}
        step_keys = [key for key in self.adsorbate_header_dict.keys() if key.startswith("step_")]

        for i, step_key in enumerate(step_keys, start=1):
            if f"step_{i}" != step_key:
                raise ValueError(f"Discontinuous reaction step {i} detected in adsorbate header.")
            else:
                name = self.adsorbate_header_dict[step_key]["name"]
                # Get adsorbate reference tag
                adsorbate_atoms = self.adsorbate_header_dict[step_key]["adsorbate_atoms"]
                reference_atoms = self.adsorbate_header_dict[step_key]["reference_atoms"]

                # Validate atom indexing list
                self._validate_poscar_ads_ref(adsorbate_atoms)
                self._validate_poscar_ads_ref(reference_atoms)

                # Check references list
                if not reference_atoms:
                    raise ValueError(f"Empty reference list found for adsorbate {name}.")

                # Regenerate adsorbate reference tag (restart reference atom indexing, 0-indexed)
                adsorbate_references[name] = self._regenerate_reference_indexing(adsorbate_atoms, reference_atoms)

        return adsorbate_references

    def generate_adsorbate_references(self, adsorbates_dict: dict, poscar_ads: List[int], poscar_ads_ref: List[int]) -> Dict[str, List[int]]:
        """
        Generate adsorbate reference points from adsorbates dict, based on adsorbate names.

        Args:
            adsorbates_dict (dict): The pre-generated adsorbate dict.
            poscar_ads (list): The adsorbate list read from config, only needed for "POSCAR" mode.
            poscar_ads_ref (list): The adsorbate reference list read from config, only needed for "POSCAR" mode.

        Returns:
            Dict[str, List[int]]: adsorbate reference atom index dict (0-indexed), the key is adsorbate name and the value being list of adsorbate atoms as reference.

        """
        # Check adsorbate dict datatype
        if not isinstance(adsorbates_dict, dict):
            raise TypeError("Wrong datatype for adsorbate dict is provided.")
        
        # Check POSCAR indexes and reference indexes data type
        if not isinstance(poscar_ads, list) or not all(isinstance(num, int) for num in poscar_ads):
            raise ValueError("Expect adsorbate indexes come in a list.")
        if not isinstance(poscar_ads_ref, list) or not all(isinstance(num, int) for num in poscar_ads_ref):
            raise ValueError("Expect adsorbate reference indexes come in a list.")

        # Generate adsorbate reference points dict based on adsorbate names
        if self.work_mode == "POSCAR":
            generated_ads_ref = self._regenerate_reference_indexing(poscar_ads, poscar_ads_ref)
            return {"adsorbate": generated_ads_ref, }

        else:  # "DATABASE" mode
            return self._load_adsorbate_ref_from_database_header()
