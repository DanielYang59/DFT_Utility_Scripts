#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import warnings
from pathlib import Path
import numpy as np
import xml.etree.ElementTree as ET
from typing import List, Tuple

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
        self.ispin = self._read_incar_tag("ISPIN")

        # Read atom list
        self.atom_list = self._read_atom_list()

        # Read fermi level
        self.fermi_level = self._read_fermi_level()

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

    def _read_atom_list(self) -> List[str]:
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

    def _parse_curve_info(self, curve_info: str) -> list:
        """
        Parses the curve information string and confirm the orbital selections to binary values.

        Parameters:
            curve_info (str): The curve information string containing orbital selections.

        Returns:
            list: A list containing the standardized curve information with binary orbital selections.
        """
        # Check curve info string
        if not isinstance(curve_info, str) or len(curve_info.split()) != 17:
            raise TypeError(f"Please check curve info line: {curve_info}.")

        curve_info = curve_info.split()

        # Standardize curve selection entry to binary integers
        standardized_curve_info = [curve_info[0], ]
        for selection in curve_info[1:]:
            if selection not in {"0", "1"}:
                raise ValueError(f"Illegal orbital selection {selection}.")

            standardized_curve_info.append(int(selection))

        return standardized_curve_info

    def _parse_atom_selection(self, atom_selections: str) -> list:
        """
        Parse atom selections.
        # NOTE: Indexing starts from 1 for single selections and element matches.

        Allowed atom selections:
        1. By index, for example: "1" (starting from 1)
        2. By index range, for example: "1-5"
        3. By element type, for example: "Fe"
        4. Mix of 1-3 separated by "_"
        5. "all" for all atoms

        Parameters:
            atom_selections (str): String representing atom selections.

        Returns:
            list: List of selected atom indices (starting from 1).
        """
        # Parse atom selections
        if atom_selections == "all":
            return list(range(1, len(self.atom_list) + 1))

        atom_selections_by_index = []
        for selection in atom_selections.split("_"):
            # Single atom selection: "1"
            if selection.isdigit():
                atom_selections_by_index.append(int(selection))

            # Range selection: "1-3"
            elif "-" in selection:
                start, end = map(int, selection.split('-'))
                atom_selections_by_index.extend(list(range(start, end + 1)))

            # Element selection: "Fe"
            else:
                atom_selections_by_index.extend([(index + 1) for index, value in enumerate(self.atom_list) if value == selection])

        assert len(atom_selections_by_index) == len(set(atom_selections_by_index)), "Duplicate atom selections detected."
        return atom_selections_by_index

    def _fetch_energy_and_pdos(self, ion_index: int, spin_index: int) -> np.ndarray:
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

        # Find the <set> element under <modeling> - <dos> - <partial> - <array>
        set_element = self.vasprun_root.find(".//dos").find(".//partial").find(".//array").find(".//set")

        # Construct the XPath to get to the specific <set> element based on ion and spin indices
        xpath_ion_spin = f".//set[@comment='ion {ion_index}']/set[@comment='spin {spin_index}']"

        # Find the specific <set> element based on ion and spin indices
        specific_set_element = set_element.find(xpath_ion_spin)

        # Convert pDOS data block to numpy array
        r_elements = specific_set_element.findall(".//r")
        return np.array([list(map(float, r.text.split())) for r in r_elements])

    def _calculate_summed_dos(self, pdos_data: np.ndarray, orbital_selections: List[int]) -> np.ndarray:
        """
        Calculate the summed DOS based orbital selections.

        Parameters:
            pdos_data (np.ndarray): The partial DOS data in shape (NEDOS, numOrbitals).
            orbital_selections (List[int]): A list of orbital selections (0 or 1) for each of the 16 orbitals.

        Returns:
            np.ndarray: The summed DOS calculated by dot product of pdos_data and orbital_selections.

        Raises:
            ValueError: If the shape of pdos_data is not (NEDOS, 16) or if orbital_selections does not have 16 elements.
        """
        # Check pDOS array shape
        nedos = int(self._read_incar_tag("NEDOS"))
        if pdos_data.ndim != 2 or pdos_data.shape not in {(nedos, 16), (nedos, 9)}:
            raise ValueError(f"Illegal pDOS array shape, expect ({nedos}, 16) or ({nedos}, 9), got {pdos_data.shape}.")

        # Calculate summed DOS
        assert all(i in {0, 1} for i in orbital_selections) and len(orbital_selections) == 16

        if pdos_data.shape[2] == 9:
            return np.dot(pdos_data, np.array(orbital_selections[:9]))

        elif pdos_data.shape[2] == 16:
            return np.dot(pdos_data, np.array(orbital_selections))

        else:
            raise RuntimeError("Unknown pDOS data shape, please report to the author.")

    def read_pdos(self, curve_info: str) -> Tuple[dict, dict]:
        """
        Reads the pDOS for selected atoms.

        Parameters:
            curve_info (str): A string containing information about the requested pDOS.

        Returns:
            dict: A dictionary where keys are atom indices and values are arrays representing the pDOS for the corresponding atoms.
        """
        # Parse curve info str
        curve_info = self._parse_curve_info(curve_info)

        # Parse atom selection list
        atom_selections = self._parse_atom_selection(curve_info[0])

        # Read pDOS of selected atoms
        pdos_dict_spin_up = {}
        pdos_dict_spin_down = {}

        for index in atom_selections:
            # Fetch pDOS (spin up)
            pdos_data_spin_up = self._fetch_energy_and_pdos(index, spin_index=1)

            # Calculate summed DOS (spin up)
            pdos_dict_spin_up[index] = self._calculate_summed_dos(pdos_data_spin_up, curve_info[1:])

            if self.ispin == "2":
                # Fetch pDOS (spin down)
                pdos_data_spin_down = self._fetch_energy_and_pdos(index, spin_index=2)

                # Calculate summed DOS (spin down)
                pdos_dict_spin_down[index] = self._calculate_summed_dos(pdos_data_spin_down, curve_info[1:])

        return pdos_dict_spin_up, pdos_dict_spin_down

# Test area
if __name__ == "__main__":
    # Import vasprun.xml file
    reader = VasprunXmlReader(vasprunXmlFile=Path("../vasprun.xml"))

    # # Test read INCAR tags
    # print(reader._read_incar_tag(tag="NEDOS"))

    # # Test read fermi level
    # print(reader._read_fermi_level())

    # # Test read atom list
    # print(reader._read_atom_list())

    # # Test parse atom selection
    # print(reader._parse_atom_selection(atom_selections="1"))
    # print(reader._parse_atom_selection(atom_selections="202"))
    # print(reader._parse_atom_selection(atom_selections="2-8"))
    # print(reader._parse_atom_selection(atom_selections="Ti"))
    # print(reader._parse_atom_selection(atom_selections="1_3-8_Ti"))
    # print(reader._parse_atom_selection(atom_selections="all"))

    # # Test parse curve info
    # print(reader._parse_curve_info(curve_info="all              0    0   0   0     0    0    0    0    0         0     0    0    0   0    0    0"))
    # print(reader._parse_curve_info(curve_info="all              1    1   1   1     1    1    1    1    1       1     1    1    1   1    1    1"))

    # # Test fetch pDOS
    # print(reader._fetch_energy_and_pdos(ion_index=1, spin_index=1))
    # print(reader._fetch_energy_and_pdos(ion_index=1, spin_index=1).shape)
    # print(reader._fetch_energy_and_pdos(ion_index=1, spin_index=2).shape)
    # print(reader._fetch_energy_and_pdos(ion_index=202, spin_index=1).shape)
    # print(reader._fetch_energy_and_pdos(ion_index=202, spin_index=2).shape)

    # Test summing pDOS
