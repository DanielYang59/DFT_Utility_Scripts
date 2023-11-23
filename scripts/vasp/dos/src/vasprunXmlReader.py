#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pathlib import Path
import numpy as np
import xml.etree.ElementTree as ET

class VasprunXmlReader:
    def __init__(self, vasprunXmlFile: Path) -> None:
        # Check config file
        if not vasprunXmlFile.is_file():
            raise FileNotFoundError("vasprun.xml file not found.")

        # Import vasprun.xml file
        vasprun_tree = ET.parse(vasprunXmlFile)
        self.vasprun_root = vasprun_tree.getroot()

    def _validate_incar_tags_for_pdos_calc(self, nedos_warn_threshold: int = 500) -> None:
        # IBRION = -1
        # NSW = 0
        # LORBIT = 11 (handle 10)

        # How to handle ISPIN = 1
        pass

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

    def read_pdos(self) -> np.ndarray:
        # Validate INCAR tags before proceeding
        self._validate_incar_tags_for_pdos_calc()

        #

    def read_energies(self) -> np.ndarray:
        pass

# Test area
if __name__ == "__main__":
    # Import vasprun.xml file
    reader = VasprunXmlReader(vasprunXmlFile=Path("../vasprun.xml"))

    # Test read INCAR tags
    nedos = reader._read_incar_tag(tag="NEDOS")
    print(nedos)

    # Test read fermi level
    fermi_level = reader.read_fermi_level()
    print(fermi_level)
