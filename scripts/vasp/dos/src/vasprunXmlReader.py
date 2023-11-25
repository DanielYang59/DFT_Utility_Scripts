#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import warnings
from pathlib import Path
import numpy as np
import xml.etree.ElementTree as ET
from typing import List

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

        # Read ISPIN tag in INCAR file
        self.ispin = self.read_incar_tag("ISPIN")

    def _validate_incar_tags_for_pdos_calc(self) -> None:
        """
        Validate INCAR tags for pDOS calculation.

        Raises:
            RuntimeError: If the IBRION, or NSW tags are not set to the expected values.
            UserWarning: If the LORBITAL tag has a value other than 11, as the script is intended for LORBITAL=11.

        This function fetches relevant INCAR tags for a pDOS calculation and checks if they are set to the expected values.
        The validation criteria are as follows:
        - IBRION should be set to -1 for "no ion updating."
        - NSW should be set to 0 for "0 ionic steps."
        - LORBITAL should be set to 11.

        """
        # Fetch related INCAR tags
        ibrion = self.read_incar_tag("IBRION")
        nsw = self.read_incar_tag("NSW")
        lorbital = self.read_incar_tag("LORBITAL")

        # IBRION tag should be -1 for "no ion updating"
        if ibrion != "-1":
            raise RuntimeError("IBRION tag should be -1.")

        # NSW tag should be 0 for "0 ionic steps"
        if nsw != "0":
            raise RuntimeError("NSW tag should be 0.")

        # LORBIT should be 11 for
        if lorbital != "11":
            warnings.warn("Script intended for LORBITAL=11, other values are not tested.")

    def read_incar_tag(self, tag: str) -> str:
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

    def read_fermi_level(self) -> float:
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

    def read_atom_list(self) -> List[str]:
        """
        Reads and returns a list of element names in the <array name="atoms"> section
        of the vasprun.xml file.

        Returns:
        list: A list containing element names.
        """
        # Get the <atominfo> section in vasprun.xml
        atom_info = self.vasprun_root.find(".//atominfo").find(".//set")

        # Initialize a list to store element names
        element_names = []

        # Iterate through <rc> elements under <set>
        for rc_element in atom_info.findall(".//rc"):
            # Find the <c> element under <rc> and get its text
            c_element = rc_element.find(".//c")
            element_name = c_element.text.strip()

            # Append the element name to the list
            element_names.append(element_name)

        assert element_names
        return element_names

    def read_energy_and_pdos(self, ion_index: int, spin_index: int) -> np.ndarray:
        """
        Extracts energy and partial density of states (pDOS) data for a specific ion and spin from the vasprun.xml file.

        Parameters:
            ion_index (int): Index of the ion (1-indexed).
            spin_index (int): Index of the spin (1 or 2).

        Returns:
            np.ndarray: Numpy array containing the extracted energy and pDOS data.

        Raises:
            ValueError: If ion_index is less than or equal to 0 (expecting 1-indexing) or if spin_index is not 1 or 2.
            TypeError: If the specific <set> element based on ion and spin indices is not found in the XML structure.

        Note:
        The returned array includes the energy values and pDOS data for the specified ion and spin.
        """
        # Check args
        if ion_index <= 0:
            raise ValueError(f"Illegal ion index {ion_index} (expect 1-indexing).")
        if spin_index not in {1, 2}:
            raise ValueError(f"Illegal spin {spin_index}.")
        if spin_index == 2 and self.ispin == "1":
            raise RuntimeError("Cannot read spin down pDOS when ISPIN is 1.")

        # Find the <set> element under <modeling> - <dos> - <partial> - <array>
        set_element = self.vasprun_root.find(".//dos").find(".//partial").find(".//array").find(".//set")

        # Construct the XPath to get to the specific <set> element based on ion and spin indices
        xpath_ion_spin = f".//set[@comment='ion {ion_index}']/set[@comment='spin {spin_index}']"

        # Find the specific <set> element based on ion and spin indices
        specific_set_element = set_element.find(xpath_ion_spin)

        # Convert pDOS data block to numpy array
        r_elements = specific_set_element.findall(".//r")
        return np.array([list(map(float, r.text.split())) for r in r_elements])

# Test area
if __name__ == "__main__":
    # Import vasprun.xml file
    reader = VasprunXmlReader(vasprunXmlFile=Path("../vasprun.xml"))

    # # Test reading INCAR tags
    # print(reader.read_incar_tag(tag="NEDOS"))

    # # Test reading fermi level
    # print(reader.read_fermi_level())

    # # Test reading atom list
    # print(reader.read_atom_list())

    # # Test fetching pDOS
    # print(reader.read_energy_and_pdos(ion_index=1, spin_index=1))
    # print(reader.read_energy_and_pdos(ion_index=1, spin_index=1).shape)
    # print(reader.read_energy_and_pdos(ion_index=1, spin_index=2).shape)
    # print(reader.read_energy_and_pdos(ion_index=202, spin_index=1).shape)
    # print(reader.read_energy_and_pdos(ion_index=202, spin_index=2).shape)
