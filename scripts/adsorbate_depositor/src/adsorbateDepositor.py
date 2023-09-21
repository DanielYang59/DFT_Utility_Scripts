#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import Union, List
from pathlib import Path
import warnings
from tqdm import tqdm
from ase import Atoms
from ase.io import read

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

    def _fix_substrate(self, poscar: Atoms, substrate_indexes: List[int]):
        """
        Fix selected atoms for selective dynamics.
        """
        # Type checks
        if not isinstance(poscar, Atoms):
            raise TypeError(f"Expected 'poscar' to be of type Atoms, but got {type(poscar)}.")

        if not isinstance(substrate_indexes, list) or not all(isinstance(i, int) for i in substrate_indexes):
            raise TypeError(f"Expected 'substrate_indexes' to be a list of integers, but got {type(substrate_indexes)}.")

        # Check that all indexes are >= 1
        if any(i < 1 for i in substrate_indexes):
            raise ValueError("All substrate indexes must be >= 1 (should be 1-indexed).")

    def _set_vacuum_level(self, new_vacuum_level: Union[float, int]):
        """
        Set vacuum level thickness.
        """
        # TODO: warning for 1st incomplete version
        warnings.warn("Current 1st version of set vacuum level is only able to handle cases where atom cluster is continuous along z-axis (vacuum level not reside on the middle of the model).")

        # Check the type of new_vacuum_level
        if not isinstance(new_vacuum_level, (float, int)):
            raise TypeError(f"Expected 'new_vacuum_level' to be of type float or int, but got {type(new_vacuum_level)}.")

        # Check the value of new_vacuum_level
        if new_vacuum_level <= 0:
            raise ValueError("Vacuum level thickness must be greater than zero.")

        # Issue a warning for small vacuum levels
        elif new_vacuum_level <= 5:
            warnings.warn(f"Small vacuum level of {new_vacuum_level} Å set.")

    def _reposition_along_z(self):
        """
        Reposition atom cluster along z-axis.
        """
        # TODO: warning for 1st incomplete version
        warnings.warn("Current 1st version of atom reposition is only able to handle cases where atom cluster is continuous along z-axis (vacuum level not reside on the middle of the model).")

    def _offset_adsorbate_along_z(self, minimal_distance: Union[float, int], direction: str = "top"):
        """
        Offset adsorbate along z-axis to maintain minimal distance.
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

        # Check the value of direction
        if direction not in {"top", "bottom"}:
            raise ValueError(f"Adsorbate offset direction should be either 'top' or 'bottom', but got {direction}.")

    def _deposit_adsorbate_on_site(self, poscar_substrate: Atoms, site: List[float], adsorbate: Atoms, ads_reference: List[int], auto_offset_along_z: bool = True) -> Atoms:
        """
        The actual worker that deposit adsorbate onto substrate site.
        NOTE: be sure NOT to sort the atom list (keep adsorbate to the end of POSCAR).
        """
        # Check args:  # TODO: clean up
        assert isinstance(poscar_substrate, Atoms)
        assert isinstance(site, list) and len(site) == 3
        assert isinstance(adsorbate, Atoms)
        assert isinstance(ads_reference, list)

        # Combine substrate and adsorbate POSCARs

        # Calculate adsorbate moving vector

    def deposit(self, target_vacuum_level: Union[float, int], auto_offset_along_z: bool = True, center_along_z: bool = True, fix_substrate: bool = False) -> dict:
        """
        Deposit adsorbates onto specified sites on the substrate.

        Args:
            target_vacuum_level (Union[float, int]): The target vacuum level in angstroms.
            auto_offset_along_z (bool, optional): Whether to automatically offset the adsorbate along the Z-axis. Defaults to True.
            center_along_z (bool, optional): Whether to center the structure along the Z-axis. Defaults to True.
            fix_substrate (bool, optional): Whether to fix the substrate atoms during deposition. Defaults to False.

        Returns:
            dict: A dictionary containing the resulting structures, indexed by a composite species name.

        Raises:
            TypeError: If the provided arguments are not of the expected types.
        """
        # Check the type and value of target_vacuum_level
        if not isinstance(target_vacuum_level, (float, int)):
            raise TypeError(f"Expected 'target_vacuum_level' to be of type float or int, but got {type(target_vacuum_level)}.")

        elif target_vacuum_level <= 5:
            warnings.warn(f"Small vacuum level of {target_vacuum_level} Å set.")

        # Check the type of boolean flags
        if not isinstance(auto_offset_along_z, bool):
            raise TypeError(f"Expected 'auto_offset_along_z' to be of type bool, but got {type(auto_offset_along_z)}.")

        if not isinstance(center_along_z, bool):
            raise TypeError(f"Expected 'center_along_z' to be of type bool, but got {type(center_along_z)}.")

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
                if center_along_z:  # Center the atom cluster along the Z-axis
                    result = self._reposition_along_z(result, mode="z_center")

                if fix_substrate:  # Freeze substrate atoms (for selective dynamics)
                    result = self._fix_substrate(result, self.poscar_substrate)

                # Compile the sample name from site and adsorbate names
                sample_name = f"{site_name}_{ads_name}"

                # Save the post-processed result
                results[sample_name] = result

        return results

    def write(self, output_dir: Path):

        """Write generated dict to file.

        Args:
            output_dir (Path): Path to the directory where output will be saved.

        """
        # Check and create the output directory
        if not isinstance(output_dir, Path):
            raise TypeError(f"Expected 'output_dir' to be of type Path, but got {type(output_dir)}.")

        if not output_dir.is_dir():
            output_dir.mkdir(parents=True)
