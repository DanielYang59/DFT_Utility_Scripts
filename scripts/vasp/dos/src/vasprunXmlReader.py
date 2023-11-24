#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pathlib import Path
import numpy as np
import xml.etree.ElementTree as ET
import warnings

class VasprunXmlReader:
    def __init__(self, vasprunXmlFile: Path) -> None:
        # Check config file
        if not vasprunXmlFile.is_file():
            raise FileNotFoundError("vasprun.xml file not found.")

        # Import vasprun.xml file
        vasprun_tree = ET.parse(vasprunXmlFile)
        self.vasprun_root = vasprun_tree.getroot()

        # Validate INCAR tags before proceeding
        self._validate_incar_tags_for_pdos_calc()

    def _validate_incar_tags_for_pdos_calc(self) -> None:
        """
        Validate INCAR tags for spin-polarized PDOS calculation.

        Raises:
            RuntimeError: If the IBRION, NSW, or ISPIN tags are not set to the expected values.
            UserWarning: If the LORBITAL tag has a value other than 11, as the script is intended for LORBITAL=11.

        This function fetches relevant INCAR tags for a PDOS calculation and checks if they are set to the expected values.
        The validation criteria are as follows:
        - IBRION should be set to -1 for "no ion updating."
        - NSW should be set to 0 for "0 ionic steps."
        - ISPIN should be set to 2 for "spin-polarized calculation."
        - LORBITAL should be set to 11.

        """
        # Fetch related INCAR tags
        ibrion = self._read_incar_tag("IBRION")
        nsw = self._read_incar_tag("NSW")
        lorbital = self._read_incar_tag("LORBITAL")
        ispin = self._read_incar_tag("ISPIN")

        # IBRION tag should be -1 for "no ion updating"
        if ibrion != "-1":
            raise RuntimeError("IBRION tag should be -1.")

        # NSW tag should be 0 for "0 ionic steps"
        if nsw != "0":
            raise RuntimeError("NSW tag should be 0.")

        # ISPIN should be 2 for "spin-polarized calculation"
        if ispin != "2":
            raise RuntimeError("ISPIN != 2 is currently not supported.")

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

    def read_pdos(self, curve_info: str) -> np.ndarray:
        """
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
        pdos_dict = {}
        for index in atom_selections:
            pdos_dict[index] = self.read_pdos(index)

        return pdos_dict

    def read_energies(self) -> np.ndarray:
        # Read energy array from vasprun.xml

        # Remember to handle fermi level
        pass

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
