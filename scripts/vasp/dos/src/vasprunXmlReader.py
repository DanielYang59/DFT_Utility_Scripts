#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pathlib import Path
import numpy as np
import xml.etree.ElementTree as ET
import warnings
from typing import List, Tuple

class VasprunXmlReader:
    def __init__(self, vasprunXmlFile: Path) -> None:
        # Check config file
        if not vasprunXmlFile.is_file():
            raise FileNotFoundError("vasprun.xml file not found.")

        # Import vasprun.xml file
        vasprun_tree = ET.parse(vasprunXmlFile)
        self.vasprun_root = vasprun_tree.getroot()

        # Read ISPIN tag in INCAR file
        self.ispin = self._read_incar_tag("ISPIN")

        # Validate INCAR tags before proceeding
        self._validate_incar_tags_for_pdos_calc()

    def _validate_incar_tags_for_pdos_calc(self) -> None:
        """
        Validate INCAR tags for PDOS calculation.

        Raises:
            RuntimeError: If the IBRION, or NSW tags are not set to the expected values.
            UserWarning: If the LORBITAL tag has a value other than 11, as the script is intended for LORBITAL=11.

        This function fetches relevant INCAR tags for a PDOS calculation and checks if they are set to the expected values.
        The validation criteria are as follows:
        - IBRION should be set to -1 for "no ion updating."
        - NSW should be set to 0 for "0 ionic steps."
        - LORBITAL should be set to 11.

        """
        # Fetch related INCAR tags
        ibrion = self._read_incar_tag("IBRION")
        nsw = self._read_incar_tag("NSW")
        lorbital = self._read_incar_tag("LORBITAL")

        # IBRION tag should be -1 for "no ion updating"
        if ibrion != "-1":
            raise RuntimeError("IBRION tag should be -1.")

        # NSW tag should be 0 for "0 ionic steps"
        if nsw != "0":
            raise RuntimeError("NSW tag should be 0.")

        # LORBIT should be 11 for
        if lorbital != "11":
            warnings.warn("Script intended for LORBITAL=11, other values are not tested.")

    def _read_incar_tag(self, tag: str) -> str:
        """
        Read the value of a specific tag within the <incar> element in the VASP vasprun.xml file.

        Parameters:
            tag (str): The name of the tag to be read from the INCAR section.

        Returns:
            str: The value of the specified tag within the INCAR section.

            If the specified tag is not found, returns None.
        """
        # Locate the <incar> element
        incar_element = self.vasprun_root.find(".//incar")

        # Find the specific tag within the <incar> element
        tag_element = incar_element.find(f".//i[@name='{tag}']")

        if tag_element is not None:
            return tag_element.text.strip()
        else:
            return None

    def _read_fermi_level(self) -> float:
        """
        Read the Fermi level in eV from the VASP vasprun.xml file.

        Returns:
            float: The Fermi level value.

        Raises:
            RuntimeError: If the <i name="efermi"> tag is not found in the <dos> element.

        This function extracts the Fermi level value from the vasprun.xml file.
        It searches for the <i name="efermi"> tag within the <dos> element and returns its float value.
        If the tag is not found, a RuntimeError is raised.

        """
        # Find the <i name="efermi"> tag within the <dos> element
        efermi_element = self.vasprun_root.find(".//dos/i[@name='efermi']")

        if efermi_element is not None:
            return float(efermi_element.text.strip())
        else:
            raise RuntimeError("Cannot find fermi level in vasprun.xml.")

    def _parse_curve_info(self, curve_info: str) -> list:
        # Convert curve info string to list
        assert isinstance(curve_info, str)

        # Check output curve info list
        assert len(curve_info) == 17
        for v in curve_info[1:]:
            assert v in {0, 1}

    def _parse_atom_selection(self, atom_selection: str) -> list:
        # Assert no duplicates
        # Make sure consistent indexing
        pass

    def _fetch_pdos(self, ion_index: int, spin_index: int) -> np.ndarray:
        # Check args
        assert ion_index >= 1
        assert spin_index in {1, 2}


    def _calculate_summed_dos(self, pdos_data: np.ndarray, orbital_selections: List[int]) -> np.ndarray:
        pass


    def read_pdos(self, curve_info: str) -> Tuple(dict, dict):
        """
        DEBUG: check return type hint
        Reads the PDOS for selected atoms.

        Parameters:
            curve_info (str): A string containing information about the requested PDOS.

        Returns:
            dict: A dictionary where keys are atom indices and values are arrays representing the PDOS for the corresponding atoms.
        """
        # Parse curve info str
        curve_info = self._parse_curve_info(curve_info)

        # Parse atom selection list
        atom_selections = self._parse_atom_selection(curve_info[0])

        # Read PDOS of selected atoms
        pdos_dict_spin_up = {}
        pdos_dict_spin_down = {}

        for index in atom_selections:
            # Fetch PDOS (spin up)
            pdos_data_spin_up = self._fetch_pdos(index, spin_index=1)

            # Calculate summed DOS (spin up)
            pdos_dict_spin_up[index] = self._calculate_summed_dos(pdos_data_spin_up, curve_info[1:])

            if self.ispin == "2":
                # Fetch PDOS (spin down)
                pdos_data_spin_down = self._fetch_pdos(index, spin_index=2)

                # Calculate summed DOS (spin down)
                pdos_dict_spin_down[index] = self._calculate_summed_dos(pdos_data_spin_down, curve_info[1:])

        return pdos_dict_spin_up, pdos_dict_spin_down

# Test area
if __name__ == "__main__":
    # Import vasprun.xml file
    reader = VasprunXmlReader(vasprunXmlFile=Path("../vasprun.xml"))

    # Test read INCAR tags
    nedos = reader._read_incar_tag(tag="NEDOS")
    print(nedos)

    # Test read fermi level
    fermi_level = reader._read_fermi_level()
    print(fermi_level)
