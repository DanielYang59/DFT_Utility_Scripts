#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pathlib import Path
from typing import Union

class SiteGenerator:
    """
    Class to handle structure generation.
    """

    def __init__(self, POSCAR_substrate: Path, distance: Union[float, int], sites: list, check_sites: bool = True) -> None:
        """
        Initialize StructureGenerator.

        Args:
            POSCAR_substrate (Path): The path to the substrate POSCAR file.
            distance (float): The distance for the structure generation.
            sites (list): A list of sites for the structure generation.
            check_sites (bool): Whether to check sites or not. Default is True.
        """
        # Check args
        if not POSCAR_substrate.is_file():
            raise FileNotFoundError("Substrate POSCAR file not found.")

        if not isinstance(distance, (float, int)):
            raise TypeError("Distance should be either a float or an integer.")

        if not isinstance(sites, list) or not sites:
            raise ValueError("sites is not list or is empty.")

        if not isinstance(check_sites, bool):
            raise TypeError("check_sites datatype should be boolean.")

        self.poscar_substrate = POSCAR_substrate
        self.sites = sites
        if check_sites:
            self._check_sites(sites)

    def _check_sites():

        pass

    def generate():
        pass


# Test area
if __name__ == "__main__":

    site_generator = SiteGenerator(
        substrate_POSCAR="/Users/yang/Developer/DFT_Utility_Scripts/scripts/adsorbate_depositor/test_dir/POSCAR_substrate",
        sites=["1", "2_3", "4_5_6", "7_8_9_10"],
        check_sites=True,
        )

    sites = site_generator.generate()
