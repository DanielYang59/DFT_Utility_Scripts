#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# TODO: show progress bar

from typing import Union, List
from pathlib import Path
import warnings
from ase import Atoms
from ase.io import read

class AdsorbateDepositor:
    """
    A class for depositing adsorbates onto substrate sites.

    Attributes:
        poscar_substrate (Path): Path to the POSCAR file representing the substrate.
        sites (dict): Dictionary of available adsorption sites on the substrate.
        adsorbates (dict): Dictionary of adsorbates to be deposited.
        output_dir (Path): Path to the directory where output files will be saved.
    """

    def __init__(self, POSCAR_substrate: Path, sites: dict, adsorbates: dict, output_dir: Path,):
        """
        Initializes an instance of AdsorbateDepositor.

        Args:
            POSCAR_substrate (Path): Path to the POSCAR file of the substrate.
            sites (dict): Dictionary containing information about the adsorption sites.
            adsorbates (dict): Dictionary containing information about the adsorbates.
            output_dir (Path): Path to the directory where output will be saved.

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

        # Check and create the output directory
        if not isinstance(output_dir, Path):
            raise TypeError(f"Expected 'output_dir' to be of type Path, but got {type(output_dir)}.")

        if not output_dir.is_dir():
            output_dir.mkdir(parents=True)

        # Parse args
        self.poscar_substrate = read(POSCAR_substrate)
        self.sites = sites
        self.adsorbates = adsorbates
        self.output_dir = output_dir

    def _fix_substrate(self, poscar: Atoms, substrate_indexes: List[int]):
        # Type checks
        if not isinstance(poscar, Atoms):
            raise TypeError(f"Expected 'poscar' to be of type Atoms, but got {type(poscar)}.")

        if not isinstance(substrate_indexes, list) or not all(isinstance(i, int) for i in substrate_indexes):
            raise TypeError(f"Expected 'substrate_indexes' to be a list of integers, but got {type(substrate_indexes)}.")

        # Check that all indexes are >= 1
        if any(i < 1 for i in substrate_indexes):
            raise ValueError("All substrate indexes must be >= 1 (should be 1-indexed).")

    def _set_vacuum_level(self, new_vacuum_level: Union[float, int]):
        # Check the type of new_vacuum_level
        if not isinstance(new_vacuum_level, (float, int)):
            raise TypeError(f"Expected 'new_vacuum_level' to be of type float or int, but got {type(new_vacuum_level)}.")

        # Check the value of new_vacuum_level
        if new_vacuum_level <= 0:
            raise ValueError("Vacuum level thickness must be greater than zero.")

        # Issue a warning for small vacuum levels
        elif new_vacuum_level <= 5:
            warnings.warn(f"Small vacuum level of {new_vacuum_level} Å set.")

    def _offset_adsorbate_along_z(self, minimal_distance: Union[float, int], direction: str = "top"):
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

    def _reposition_along_z(self):
        pass

    def _deposit_adsorbate_on_site(self, poscar_substrate, site, adsorbate):
        pass

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
        for site_name, site_info in self.sites.items():
            for ads_name, ads_info in self.adsorbates.items():
                # Compile the sample name from site and adsorbate names
                sample_name = f"{site_name}_{ads_name}"

                # Perform the actual deposition
                results[sample_name] = self._deposit_adsorbate_on_site(self.poscar_substrate, site_info, ads_info)

        return results
