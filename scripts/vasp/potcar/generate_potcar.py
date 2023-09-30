#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from pathlib import Path
import warnings
from typing import List

class PotcarGenerator:
    """
    PotcarGenerator class responsible for generating POTCAR files based on a list of elements.

    Attributes:
        potcar_lib (Path): A Path object representing the directory where the POTCAR library resides.

    Methods:
        generate_potcar(elements: List[str], output_potcarfile: Path = Path("POTCAR")) -> None:
            Generates a POTCAR file based on a list of elements.
        get_elements_from_poscar(poscarfile: Path) -> List[str]:
            Retrieves the list of elements from a given POSCAR file.
        get_potcar_lib() -> Path:
            Obtains the POTCAR library path from the environment variable.
    """

    def __init__(self):
        """
        Initialize the PotcarGenerator class.
        """
        self.potcar_lib = self.get_potcar_library_path()

    def get_elements_from_poscar(self, poscarfile: Path) -> list:
        """
        Get the list of elements from a POSCAR file.

        Parameters:
            poscarfile (Path): Path to the POSCAR file.

        Returns:
            list: List of elements.

        Raises:
            FileNotFoundError: If the specified POSCAR file does not exist.
            RuntimeError: If the elements list in the POSCAR file is empty.
        """
        if not poscarfile.is_file():
            raise FileNotFoundError(f"The POSCAR file {poscarfile} does not exist.")

        with poscarfile.open('r', encoding="utf-8") as f:
            lines = f.readlines()
        elements = lines[5].strip().split()

        if not elements:
            raise RuntimeError("The elements list is empty. Check your POSCAR file.")

        return elements

    def get_potcar_library_path(self) -> Path:
        """
        Get the path to the POTCAR library from the environment variable.

        Returns:
            Path: Path to the POTCAR library.

        Raises:
            EnvironmentError: If the POTCAR_LIBRARY_PATH environment variable is not set.
            FileNotFoundError: If the path specified in the environment variable does not exist or is not a directory.
        """
        POTCAR_LIBRARY_PATH = os.environ.get("POTCAR_LIBRARY_PATH")
        if POTCAR_LIBRARY_PATH is None:
            raise EnvironmentError(
                "The POTCAR_LIBRARY_PATH environment variable is not set. "
                "Please set this variable to the path of your POTCAR library."
            )

        potcar_path = Path(POTCAR_LIBRARY_PATH)
        if not potcar_path.is_dir():
            raise FileNotFoundError(
                f"The path specified in POTCAR_LIBRARY_PATH ({POTCAR_LIBRARY_PATH}) either does not exist "
                "or is not a directory. Please check the path and try again."
            )

        return potcar_path

    def generate_potcar(self, elements: List[str], output_potcarfile: Path = Path("POTCAR"), max_elements: int = 20) -> None:
        """
        Generate a POTCAR file based on a list of elements.

        Parameters:
            elements (list): A list containing the chemical symbols of the elements.
            output_potcarfile (Path): A Path object for the output POTCAR file. Defaults to 'POTCAR' in the current directory.

        Raises:
            FileNotFoundError: If POTCAR for any of the specified elements is not found in the library.
        """
        # Check for warnings related to large number of elements
        if len(elements) >= max_elements:
            warnings.warn(f"The elements list contains more than {max_elements} elements. Proceed with caution.")

        # Check for valid elements
        valid_elements = ["H", "He", "Li", "Be", "B", "C", "N", "O", "F", "Ne", "Na", "Mg", "Al", "Si", "P", "S", "Cl", "Ar", "K", "Ca", "Sc", "Ti", "V", "Cr", "Mn", "Fe", "Co", "Ni", "Cu", "Zn", "Ga", "Ge", "As", "Se", "Br", "Kr", "Rb", "Sr", "Y", "Zr", "Nb", "Mo", "Tc", "Ru", "Rh", "Pd", "Ag", "Cd", "In", "Sn", "Sb", "Te", "I", "Xe", "Cs", "Ba", "La", "Ce", "Pr", "Nd", "Pm", "Sm", "Eu", "Gd", "Tb", "Dy", "Ho", "Er", "Tm", "Yb", "Lu", "Hf", "Ta", "W", "Re", "Os", "Ir", "Pt", "Au", "Hg", "Tl", "Pb", "Bi", "Th", "Pa", "U", "Np", "Pu", "Am", "Cm", "Bk", "Cf", "Es", "Fm", "Md", "No", "Lr", "Rf", "Db", "Sg", "Bh", "Hs", "Mt", "Ds", "Rg", "Cn", "Nh", "Fl", "Mc", "Lv", "Ts", "Og"]
        for element in elements:
            if element not in valid_elements:
                raise ValueError(f"{element} is not a valid chemical element.")

        # Initialize an empty string to store POTCAR data
        potcar_data = ""

        for element in elements:
            element_potcar_path = self.potcar_lib / element / "POTCAR"

            # Check if POTCAR file for the element exists
            if not element_potcar_path.is_file():
                raise FileNotFoundError(f"POTCAR for {element} not found in {self.potcar_lib}.")

            # Write output POTCAR file
            with element_potcar_path.open("r", encoding="utf-8") as f:
                potcar_data += f.read()

        # Write the combined POTCAR data to the output path
        with output_potcarfile.open("w", encoding="utf-8") as f:
            f.write(potcar_data)

def main(poscarfile: Path = Path("POSCAR")) -> None:
    """
    Main function to create a POTCAR file based on elements listed in a POSCAR file.

    Parameters:
        poscarfile (Path): Path to the POSCAR file. Defaults to 'POSCAR' in the current directory.
    """
    potcar_gen = PotcarGenerator()
    elements = potcar_gen.get_elements_from_poscar(poscarfile)
    potcar_gen.generate_potcar(elements)

if __name__ == "__main__":
    main()
