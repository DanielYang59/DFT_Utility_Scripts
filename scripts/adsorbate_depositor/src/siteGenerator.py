#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pathlib import Path
from typing import Union, List
import numpy as np
from ase.io import read
import warnings

class SiteGenerator:
    """
    Class responsible for generating various site positions on a substrate based on the given POSCAR file.
    """

    def __init__(self, POSCAR_substrate: Path, distance: Union[float, int], sites: List[str]) -> None:
        """
        Initialize the SiteGenerator object with the path to the substrate's POSCAR file, distance, and sites.

        Args:
            POSCAR_substrate (Path): File path to the substrate's POSCAR file.
            distance (Union[float, int]): Vertical distance from the substrate for the generated site.
            sites (List[str]): List of site identifiers, each a string.

        Raises:
            FileNotFoundError: If the POSCAR file is not found.
            TypeError: If distance is not a float or integer.
            ValueError: If the sites list is empty, or distance is non-positive.
        """
        # Validation
        if not POSCAR_substrate.is_file():
            raise FileNotFoundError("Substrate POSCAR file not found.")

        if not isinstance(distance, (float, int)):
            raise TypeError("Distance should be either a float or an integer.")

        if distance <= 0:
            raise ValueError("Distance could not be zero or negative.")
        elif distance <= 1:
            warnings.warn(f"Small distance of {distance} Å found. Make sure this is what you want.")

        if not isinstance(sites, list) or not sites:
            raise ValueError("Sites must be a non-empty list.")

        self.poscar_substrate = POSCAR_substrate
        self.distance = distance
        self.sites = sites

    def _check_site(self, site_str: str) -> List[int]:
        """
        Validate the site string and return the parsed components.

        Args:
            site_str (str): String identifier for the site.

        Returns:
            List[int]: List of integers parsed from site_str.

        Raises:
            TypeError: If site_str is not a string.
            ValueError: If site_str contains invalid or duplicate values.
        """
        if not isinstance(site_str, str):
            raise TypeError(f"site_str must be a string, got {type(site_str).__name__}")

        site_components = [int(i) for i in site_str.split('_')]

        if len(site_components) != len(set(site_components)):
            raise ValueError(f"Duplicate integers found in site_str: {site_str}")

        atoms = read(self.poscar_substrate, format="vasp")
        for site in site_components:
            if site not in range(1, len(atoms) + 1):
                raise ValueError(f"Site \"{site}\" not found in POSCAR (indexing starts from 1).")

        return site_components

    def _calculate_centroid(self, atom_positions: List[List[float]]) -> List[float]:
        """
        Compute the centroid of the given atom positions.

        Args:
            atom_positions (List[List[float]]): List of Cartesian coordinates of atoms.

        Returns:
            List[float]: Cartesian coordinates of the centroid.

        Raises:
            ValueError: If the list of atom positions is empty.
        """
        if not atom_positions:
            raise ValueError("The list of atom positions cannot be empty.")

        return np.mean(np.array(atom_positions), axis=0).tolist()

    def _calculate_site(self, site_str: str, direction: str = "z_top") -> List[float]:
        """
        Compute the position for the given site string.

        Args:
            site_str (str): String identifier for the site.
            direction (str, optional): Specifies where the site should be generated. Defaults to "z_top".

        Returns:
            List[float]: Cartesian coordinates of the calculated site.

        Raises:
            ValueError: If the direction argument is invalid.
        """
        if direction not in {"z_top", "z_bottom"}:
            raise ValueError(f"Illegal site direction {direction}.")

        site_components = self._check_site(site_str)

        atoms = read(self.poscar_substrate, format="vasp")
        if len(site_components) == 1:
            position = atoms.positions[site_components[0] - 1].tolist()
        else:
            atom_positions = [atoms.positions[i - 1] for i in site_components]
            position = self._calculate_centroid(atom_positions)

        position[2] += self.distance if direction == "z_top" else -self.distance

        return position

    def generate(self) -> dict:
        """
        Generate the site positions for all site identifiers in `self.sites`.

        Returns:
            dict: A dictionary mapping each site identifier to its Cartesian coordinates.
        """
        return {f"site-{site}": self._calculate_site(site) for site in self.sites}
