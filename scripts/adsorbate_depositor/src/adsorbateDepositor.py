#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from typing import List, Dict, Union
from pathlib import Path
import warnings
from tqdm import tqdm
import numpy as np
from ase import Atoms
from ase.io import read, write
from ase.constraints import FixAtoms

# Import external vacuum layer manager
sys.path.append(str(Path(__file__).resolve().parents[3] / "vasp" / "poscar"))
from vacuumLayerManager import VacuumLayerManager

TAG_DESCRIPTIONS = {
    0: "substrate",
    1: "adsorbate"
}

class AdsorbateDepositor:
    """
    A class for depositing adsorbates onto substrate sites.

    Attributes:
        poscar_substrate (Path): Path to the POSCAR file representing the substrate.
        sites (dict): Dictionary of available adsorption sites on the substrate.
        adsorbates (dict): Dictionary of adsorbates to be deposited.
        adsorbate_refs (dict): Dictionary of adsorbate reference points.

    Notes:
        - The `_deposit_adsorbate_on_site` method handles atom tagging, where atoms are tagged as 'substrate' or 'adsorbate'.
        - For detailed information on atom tagging and how to control it, refer to the docstring of `_deposit_adsorbate_on_site`.
    """

    def __init__(self, distance: Union[float, int], POSCAR_substrate: Path, sites: dict, adsorbates: dict, adsorbate_refs: dict) -> None:
        """
        Initializes an instance of AdsorbateDepositor.

        Args:
            distance (Union[float, int]): Vertical distance from the substrate for the generated site.
            POSCAR_substrate (Path): Path to the POSCAR file of the substrate.
            sites (dict): Dictionary containing information about the adsorption sites.
            adsorbates (dict): Dictionary containing information about the adsorbates.
            adsorbate_refs (dict): Dictionary containing information about the adsorbate reference points.

        Raises:
            FileNotFoundError: If the POSCAR file is not found.
            TypeError: If the provided arguments are not of the expected types.
            ValueError: If the provided dictionaries for sites or adsorbates are empty.
        """
        # Check if distance is rational
        if not isinstance(distance, (float, int)):
            raise TypeError("Expect distance in float or int type.")
        if distance <= 0:
            raise ValueError("Distance should be greater than zero.")
        elif distance <= 1:
            warnings.warn(f"Small distance of {distance} Å found.")

        # Check if the POSCAR file exists
        if not POSCAR_substrate.is_file():
            raise FileNotFoundError(f"POSCAR file at {POSCAR_substrate} not found.")

        # Check the type and content of sites and adsorbates
        if not isinstance(sites, dict):
            raise TypeError(f"Expected 'sites' to be of type dict, but got {type(sites)}.")
        if not sites:
            raise ValueError("Got an empty sites dictionary.")

        if not isinstance(adsorbates, dict):
            raise TypeError(f"Expected 'adsorbates' to be of type dict, but got {type(adsorbates)}.")
        if not adsorbates:
            raise ValueError("Got an empty adsorbates dictionary.")

        # Parse args
        self.distance = distance
        self.poscar_substrate = read(POSCAR_substrate)
        self.sites = sites
        self.adsorbates = adsorbates
        self.adsorbate_refs = adsorbate_refs

    def _calculate_centroid(self, adsorbate: Atoms, ads_reference: List[int]) -> np.ndarray:
        """Calculate the centroid of given atom indices in the adsorbate."""
        positions = [adsorbate[index].position for index in ads_reference]
        return np.mean(positions, axis=0)

    def _fix_substrate(self, poscar: Atoms) -> Atoms:
        """
        Fix atoms tagged as substrate (tag=0) for selective dynamics.

        Args:
            poscar (Atoms): The Atoms object representing the structure.

        Returns:
            Atoms: The Atoms object with fixed substrate atoms.

        Notes:
            - The function uses integer tags to identify atoms. Specifically, atoms with tag 0 are considered 'substrate' and atoms with tag 1 are considered 'adsorbate'.
        """

        # Type checks
        if not isinstance(poscar, Atoms):
            raise TypeError(f"Expected 'poscar' to be of type Atoms, but got {type(poscar)}.")

        # Define tag description
        tag_descriptions = {
            0: "substrate",
            1: "adsorbate"
        }

        # Get indices of substrate atoms
        substrate_indices = [atom.index for atom in poscar if atom.tag == 0]  # 0 is the tag for "substrate"

        # Set constraints to fix substrate atoms
        constraint = FixAtoms(indices=substrate_indices)
        poscar.set_constraint(constraint)

        return poscar

    def _deposit_adsorbate_on_site(self, poscar_substrate: Atoms, site: List[float], adsorbate: Atoms, ads_reference: List[int], override_tags: bool = True) -> Atoms:
        """
        Deposits the adsorbate onto the substrate site.

        Args:
            poscar_substrate (Atoms): The Atoms object of the substrate.
            site (List[float]): The coordinates of the adsorption site.
            adsorbate (Atoms): The Atoms object of the adsorbate.
            ads_reference (List[int]): List of atom indexes to use as the reference for positioning.
            override_tags (bool, optional): Whether to override the existing atom tags. Defaults to True.

        Returns:
            Atoms: The resulting Atoms object after adsorbate deposition.

        Notes:
            - Atoms with tag 0 are considered 'substrate' and atoms with tag 1 are considered 'adsorbate'.
            - If 'override_tags' is True, the tags for substrate and adsorbate atoms will be set to 0 and 1 respectively, overriding any existing tags.
        """
        # Check args
        if not isinstance(poscar_substrate, Atoms):
            raise TypeError("Wrong datatype for substrate POSCAR.")
        if not isinstance(adsorbate, Atoms):
            raise TypeError("Wrong datatype for adsorbate POSCAR.")
        if not isinstance(site, list) or len(site) != 3:
            raise RuntimeError("Wrong site datatype or length.")
        if not isinstance(ads_reference, list):
            raise TypeError("Wrong adsorbate reference point list datatype.")
        if not isinstance(override_tags, bool):
            raise TypeError("Expected 'override_tags' to be of type bool.")

        # Override tags if requested
        if override_tags:
            for atom in poscar_substrate:
                atom.tag = 0
            for atom in adsorbate:
                atom.tag = 1

        # Calculate centroid of adsorbate reference atoms
        centroid = self._calculate_centroid(adsorbate, ads_reference)

        # Calculate vector to translate centroid to target site
        translation_vec = np.array(site) - centroid

        # Translate all atoms in the adsorbate to the target site
        for atom in adsorbate:
            atom.position += translation_vec

        # Move adsorbate up along the z-axis
        for atom in adsorbate:
            atom.position[2] += self.distance

        # Combine substrate and adsorbate
        return poscar_substrate + adsorbate

    def _check_and_adjust_distance(self, combined: Atoms, step: float = 0.01, max_move_distance: float = 25.0) -> Atoms:
        """
        Check and adjust the z-distance between adsorbate and substrate atoms.

        Parameters:
            combined (Atoms): The combined Atoms object for the substrate and adsorbate.
            step (float, optional): The distance to move the adsorbate up along the z-axis in each step. Defaults to 0.01.
            max_move_distance (float, optional): The maximum distance the adsorbate can be moved up along the z-axis to avoid potential infinite loop. Defaults to 25.0.

        Returns:
            Atoms: The adjusted combined Atoms object.
        """
        substrate_atoms = [atom for atom in combined if atom.tag == 0]
        adsorbate_atoms = [atom for atom in combined if atom.tag == 1]

        moved_distance = 0.0

        while moved_distance < max_move_distance:
            min_distance = min(np.linalg.norm(a.position - s.position) for a in adsorbate_atoms for s in substrate_atoms)

            if min_distance >= self.distance:
                break

            # Move adsorbate up along z-axis by step
            for atom in adsorbate_atoms:
                atom.position[2] += step

            moved_distance += step

        if moved_distance >= max_move_distance:
            raise RuntimeError(f"Maximum moving distance of {max_move_distance} Å reached but still cannot find a valid location. Please check your structure.")

        return combined

    def _reset_vacuum_layer_thickness(self, poscar: Atoms, target_vacuum_layer: float, vacuum_warning_threshold: float = 5.0) -> Atoms:
        """
        Reset the thickness of the vacuum layer in a given atomic structure.

        Parameters:
            poscar (Atoms): The atomic structure represented as an ASE.Atoms object.
            target_vacuum_layer (float): The target thickness for the vacuum layer in Angstroms.
            vacuum_warning_threshold (float, optional): The threshold below which a warning is raised about a potentially too small vacuum layer thickness. Default is 5.0 Angstroms.

        Returns:
            Atoms: The adjusted atomic structure with the new vacuum layer thickness.

        Raises:
            TypeError: If 'poscar' is not an ASE.Atoms object or if 'target_vacuum_layer' is not a float or int.
            ValueError: If 'target_vacuum_layer' is less than or equal to zero.
        """
        # Check poscar datatype
        if not isinstance(poscar, Atoms):
            raise TypeError(f"Expect structure in ASE.Atoms, got {type(poscar)}.")

        # Check target vacuum layer thickness
        if not isinstance(target_vacuum_layer, (float, int)):
            raise TypeError(f"Expect target vacuum layer thickness in float/int, got {type(target_vacuum_layer)}.")

        if target_vacuum_layer <= 0:
            raise ValueError("Target vacuum layer thickness cannot be smaller than zero.")
        elif target_vacuum_layer <= vacuum_warning_threshold:
            warnings.warn(f"Small vacuum thickness of {target_vacuum_layer} Å requested.")

        # Call external module to adjust vacuum layer thickness along z-axis
        vacuum_manager = VacuumLayerManager(input_structure=poscar, axis="z")
        vacuum_manager.adjust_vacuum_thickness(new_vacuum=target_vacuum_layer)

        return poscar

    def deposit(self, auto_offset_along_z: bool = True, fix_substrate: bool = False,  target_vacuum_layer: float = 10.0, vacuum_layer_warn_threshold: float = 5.0) -> dict:
        """
        Deposit adsorbates onto specified sites on the substrate.

        Args:
            auto_offset_along_z (bool, optional): Whether to automatically offset the adsorbate along the z-axis. Defaults to True.
            fix_substrate (bool, optional): Whether to fix the substrate atoms during deposition. Defaults to False.
            target_vacuum_layer (float, optional): Final vacuum layer thickness in Å.
            vacuum_layer_warn_threshold (float, optional): Vacuum layer thickness to generate warning.

        Returns:
            dict: A dictionary containing the resulting structures, indexed by a composite species name.

        Raises:
            TypeError: If the provided arguments are not of the expected types.
        """

        # Check the type of boolean flags
        if not isinstance(auto_offset_along_z, bool):
            raise TypeError(f"Expected 'auto_offset_along_z' to be of type bool, but got {type(auto_offset_along_z)}.")

        if not isinstance(fix_substrate, bool):
            raise TypeError(f"Expected 'fix_substrate' to be of type bool, but got {type(fix_substrate)}.")

        # Check target vacuum layer datatype and thickness
        if not isinstance(target_vacuum_layer, (float, int)):
            raise TypeError(f"Expected 'target_vacuum_layer' to be of type float/int, but got {type(target_vacuum_layer)}.")

        if target_vacuum_layer <= 0:
            raise ValueError("Vacuum layer thickness should be equal or greater than zero.")
        elif target_vacuum_layer <= vacuum_layer_warn_threshold:
            warnings.warn(f"Small vacuum layer thickness of {target_vacuum_layer} Å found.")

        # Deposit adsorbates onto sites
        results = {}
        for site_name, site_info in tqdm(self.sites.items(), desc="Depositing adsorbates"):
            for ads_name, ads_info in self.adsorbates.items():
                # Compile adsorbate reference tag
                ads_reference = self.adsorbate_refs[ads_name]

                # Perform the actual deposition
                result = self._deposit_adsorbate_on_site(self.poscar_substrate, site_info, ads_info, ads_reference)

                # (Optional) offset adsorbate along z-axis
                if auto_offset_along_z:
                    result = self._check_and_adjust_distance(result)

                # Reset vacuum layer thickness (would recenter atoms along z-axis)
                result = self._reset_vacuum_layer_thickness(result, target_vacuum_layer)

                # (Optional) freeze substrate atoms for selective dynamics
                if fix_substrate:
                    result = self._fix_substrate(result, self.poscar_substrate)

                # Compile the sample name from site and adsorbate names
                sample_name = f"{site_name}_{ads_name}"

                # Save the post-processed result
                results[sample_name] = result

        return results

    def write(self, atoms_dict: Dict[str, Atoms], output_dir: Path, filename: str = "POSCAR_generated") -> None:
        """
        Write generated Atoms objects to file, each in a separate directory based on its adsorbate name.

        Args:
            atoms_dict (Dict[str, Atoms]): Dictionary of adsorbate names and their corresponding Atoms objects.
            output_dir (Path): Directory where the Atoms objects will be saved.
            filename (str, optional): Filename for the output. Defaults to "POSCAR_generated".
        """
        # Check and create the output directory
        if not isinstance(output_dir, Path):
            raise TypeError(f"Expected 'output_dir' to be of type Path, but got {type(output_dir)}.")

        if not output_dir.is_dir():
            output_dir.mkdir(parents=True)

        # Iterate through the dictionary and write each Atoms object to its corresponding directory
        for adsorbate_name, atoms in atoms_dict.items():
            if not isinstance(atoms, Atoms):
                raise TypeError(f"Wrong datatype for {adsorbate_name}. Expected Atoms, but got {type(atoms)}.")

            adsorbate_dir = output_dir / adsorbate_name
            if not adsorbate_dir.is_dir():
                adsorbate_dir.mkdir()

            write(adsorbate_dir / filename, atoms, format="vasp")
