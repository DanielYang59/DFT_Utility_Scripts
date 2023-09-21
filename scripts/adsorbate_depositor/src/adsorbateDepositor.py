#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import List
from pathlib import Path
import warnings
from tqdm import tqdm
from ase import Atoms
from ase.io import read, write
from ase.constraints import FixAtoms

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
    """

    def __init__(self, POSCAR_substrate: Path, sites: dict, adsorbates: dict, adsorbate_refs: dict):
        """
        Initializes an instance of AdsorbateDepositor.

        Args:
            POSCAR_substrate (Path): Path to the POSCAR file of the substrate.
            sites (dict): Dictionary containing information about the adsorption sites.
            adsorbates (dict): Dictionary containing information about the adsorbates.
            adsorbate_refs (dict): Dictionary containing information about the adsorbate reference points.

        Raises:
            FileNotFoundError: If the POSCAR file is not found.
            TypeError: If the provided arguments are not of the expected types.
            ValueError: If the provided dictionaries for sites or adsorbates are empty.
        """
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
        self.poscar_substrate = read(POSCAR_substrate)
        self.sites = sites
        self.adsorbates = adsorbates
        self.adsorbate_refs = adsorbate_refs

    def _fix_substrate(self, poscar: Atoms, substrate_indexes: List[int]) -> Atoms:
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

        if not isinstance(substrate_indexes, list) or not all(isinstance(i, int) for i in substrate_indexes):
            raise TypeError(f"Expected 'substrate_indexes' to be a list of integers, but got {type(substrate_indexes)}.")

        # Check that all indexes are >= 1
        if any(i < 1 for i in substrate_indexes):
            raise ValueError("All substrate indexes must be >= 1 (should be 1-indexed).")

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

    def _offset_adsorbate_along_z(self, poscar: Atoms, minimal_distance: float = 1.5) -> Atoms:
        """
        Offset adsorbate along z-axis to maintain minimal distance.

        Args:
            poscar (Atoms): The Atoms object.
            minimal_distance (float): The minimal distance to maintain along the Z-axis.

        Returns:
            Atoms: The Atoms object with offset adsorbate.

        Notes:
            - This function only offsets atoms with tag 1, which are considered 'adsorbate'.
        """
        # Check the type of minimal_distance
        if not isinstance(minimal_distance, (float, int)):
            raise TypeError(f"Expected 'minimal_distance' to be of type float or int, but got {type(minimal_distance)}.")

        # Check the value of minimal_distance
        if minimal_distance <= 0:
            raise ValueError("Adsorbate-substrate distance must be greater than zero.")

        # Issue a warning for small adsorbate-substrate distances
        elif minimal_distance <= 1:
            warnings.warn(f"Small adsorbate-substrate distance of {minimal_distance} Å set.")

        # Filter only adsorbate atoms (tag=1)
        adsorbate_atoms = [atom for atom in poscar if atom.tag == 1]

        if not adsorbate_atoms:
            return poscar

        # Determine the minimum z-coordinate among the adsorbate atoms
        z_min = min(atom.position[2] for atom in adsorbate_atoms)

        # Calculate the amount by which to offset the adsorbate atoms along z
        offset = minimal_distance - z_min

        # Apply the offset to adsorbate atoms
        for atom in adsorbate_atoms:
            atom.position[2] += offset

        return poscar

    def _deposit_adsorbate_on_site(self, poscar_substrate: Atoms, site: List[float], adsorbate: Atoms, ads_reference: List[int]) -> Atoms:
        """
        Deposits the adsorbate onto the substrate site.

        Args:
            poscar_substrate (Atoms): The Atoms object of the substrate.
            site (List[float]): The coordinates of the adsorption site.
            adsorbate (Atoms): The Atoms object of the adsorbate.
            ads_reference (List[int]): List of atom indexes to use as the reference for positioning.

        Returns:
            Atoms: The resulting Atoms object after adsorbate deposition.

        Notes:
            - Atoms with tag 0 are considered 'substrate' and atoms with tag 1 are considered 'adsorbate'.
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

        # Tag all substrate atoms with 0
        for atom in poscar_substrate:
            atom.tag = 0

        # Tag all adsorbate atoms with 1
        for atom in adsorbate:
            atom.tag = 1

        # Combine substrate and adsorbate
        return poscar_substrate + adsorbate

    def deposit(self, auto_offset_along_z: bool = True, fix_substrate: bool = False) -> dict:
        """
        Deposit adsorbates onto specified sites on the substrate.

        Args:
            auto_offset_along_z (bool, optional): Whether to automatically offset the adsorbate along the Z-axis. Defaults to True.
            fix_substrate (bool, optional): Whether to fix the substrate atoms during deposition. Defaults to False.

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

        # Deposit adsorbates onto sites
        results = {}
        for site_name, site_info in tqdm(self.sites.items(), desc="Depositing adsorbates"):
            for ads_name, ads_info in self.adsorbates.items():
                # Compile adsorbate reference tag
                ads_reference = self.adsorbate_refs[ads_name]

                # Perform the actual deposition
                result = self._deposit_adsorbate_on_site(self.poscar_substrate, site_info, ads_info, ads_reference, auto_offset_along_z)

                # Optional post-processing steps
                ##  Offset adsorbate along z-axis
                if auto_offset_along_z:
                    self._offset_adsorbate_along_z(result, minimal_distance=2.0)

                ## Freeze substrate atoms (for selective dynamics)
                if fix_substrate:
                    result = self._fix_substrate(result, self.poscar_substrate)

                # Compile the sample name from site and adsorbate names
                sample_name = f"{site_name}_{ads_name}"

                # Save the post-processed result
                results[sample_name] = result

        return results

    def write(self, atoms: Atoms, output_dir: Path, filename: str = "POSCAR_generated"):
        """
        Write generated Atoms object to file.

        Args:
            atoms (Atoms): The Atoms object to write.
            output_dir (Path): Directory where the Atoms object will be saved.
            filename (str, optional): Filename for the output. Defaults to "POSCAR_generated".
        """
        # Check structure file datatype
        if not isinstance(atoms, Atoms):
            raise TypeError("Wrong datatype to write.")

        # Check and create the output directory
        if not isinstance(output_dir, Path):
            raise TypeError(f"Expected 'output_dir' to be of type Path, but got {type(output_dir)}.")

        if not output_dir.is_dir():
            output_dir.mkdir(parents=True)

        # Write ase.Atoms to file
        write(output_dir / filename, atoms, format="vasp")
