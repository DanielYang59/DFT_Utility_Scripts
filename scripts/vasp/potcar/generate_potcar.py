#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import os
from pathlib import Path
import warnings
from typing import List, Dict
import yaml

class PotcarGenerator:
    """
    PotcarGenerator class responsible for generating POTCAR files based on a list of elements.

    Attributes:
        potcar_lib (Path): A Path object representing the directory where the POTCAR library resides.

    Methods:
        _get_potcar_lib() -> Path:
            Obtains the POTCAR library path from the environment variable.
        generate_potcar(elements: List[str], output_potcarfile: Path = Path("POTCAR")) -> None:
            Generates a POTCAR file based on a list of elements.
        get_elements_from_poscar(poscarfile: Path) -> List[str]:
            Retrieves the list of elements from a given POSCAR file.
    """

    def __init__(self) -> None:
        """
        Initialize the PotcarGenerator class.
        """
        self.potcar_lib = self._get_potcar_library_path()

    def _get_potcar_library_path(self) -> Path:
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

    def _load_recommended_potentials(self, potential_file: Path = Path("recommended_paw_potentials.yaml")) -> Dict[str, str]:
        """
        Load VASP recommended PAW potentials from a YAML file.

        Parameters:
            potential_file (Path, optional): Path to the YAML file containing recommended PAW potentials. Defaults to "recommended_paw_potentials.yaml".

        Returns:
            Dict[str, str]: A dictionary mapping element names to the recommended PAW potentials.

        Raises:
            FileNotFoundError: If the specified potential_file is not found.
        """
        # Recompile potential path
        d = Path(__file__).resolve().parent
        potential_file = d / potential_file

        if not potential_file.is_file():
            raise FileNotFoundError(f"VASP recommended potential file {potential_file} not found.")

        with open(potential_file) as f:
            data = yaml.safe_load(f)

        return data

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

    def generate_potcar(self, elements: List[str], output_potcarfile: Path = Path("POTCAR"), warn_element_num: int = 20, fetch_recommended: bool = False, verbose: bool = True) -> None:
        """
        Generate a POTCAR file based on a list of elements.

        Parameters:
            elements (list): A list containing the chemical symbols of the elements.
            output_potcarfile (Path): A Path object for the output POTCAR file. Defaults to 'POTCAR' in the current directory.
            warn_element_num (int, Optional): The number of element count threshold to generate "too many elements" warning. Defaults to 20.
            fetch_recommended (bool, Optional): Fetch VASP recommended PAW potentials from "recommended_paw_potentials.yaml" file. Defaults to False.
            verbose (bool, Optional): Print list of elements. Defaults to True.

        Raises:
            FileNotFoundError: If POTCAR for any of the specified elements is not found in the library.
        """
        # Check for warnings related to large number of elements
        if len(elements) >= warn_element_num:
            warnings.warn(f"The elements list contains more than {warn_element_num} elements. Proceed with caution.")

        # Check for valid elements
        valid_elements = ["H", "He", "Li", "Be", "B", "C", "N", "O", "F", "Ne", "Na", "Mg", "Al", "Si", "P", "S", "Cl", "Ar", "K", "Ca", "Sc", "Ti", "V", "Cr", "Mn", "Fe", "Co", "Ni", "Cu", "Zn", "Ga", "Ge", "As", "Se", "Br", "Kr", "Rb", "Sr", "Y", "Zr", "Nb", "Mo", "Tc", "Ru", "Rh", "Pd", "Ag", "Cd", "In", "Sn", "Sb", "Te", "I", "Xe", "Cs", "Ba", "La", "Ce", "Pr", "Nd", "Pm", "Sm", "Eu", "Gd", "Tb", "Dy", "Ho", "Er", "Tm", "Yb", "Lu", "Hf", "Ta", "W", "Re", "Os", "Ir", "Pt", "Au", "Hg", "Tl", "Pb", "Bi", "Th", "Pa", "U", "Np", "Pu", "Am", "Cm", "Bk", "Cf", "Es", "Fm", "Md", "No", "Lr", "Rf", "Db", "Sg", "Bh", "Hs", "Mt", "Ds", "Rg", "Cn", "Nh", "Fl", "Mc", "Lv", "Ts", "Og"]
        for element in elements:
            if element not in valid_elements:
                raise ValueError(f"{element} is not a valid chemical element.")

        # Load VASP recommended potentials
        recommended_potentials = self._load_recommended_potentials()

        # Initialize an empty string to store POTCAR data
        potcar_data = ""

        for element in elements:
            # Get VASP recommended potentials if required
            if fetch_recommended and element in recommended_potentials.keys():
                element = recommended_potentials[element]
                warnings.warn(f"VASP recommended PAW potential {element} loaded.")

            element_potcar_path = self.potcar_lib / element / "POTCAR"

            # Check if POTCAR file for the element exists
            if not element_potcar_path.is_file():
                raise FileNotFoundError(f"POTCAR for {element} not found in {self.potcar_lib}.")

            # Write output POTCAR file
            with element_potcar_path.open("r", encoding="utf-8") as f:
                potcar_data += f.read()

        # Print element list
        if verbose:
            print(f"POTCAR for elements: '{','.join(elements)}' generated.")

        # Write the combined POTCAR data to the output path
        with output_potcarfile.open("w", encoding="utf-8") as f:
            f.write(potcar_data)

def main(poscarfile: Path = Path("POSCAR")) -> None:
    """
    Main function to create a POTCAR file based on elements listed in a POSCAR file.

    Parameters:
        poscarfile (Path): Path to the POSCAR file. Defaults to 'POSCAR' in the current directory.
    """
    # Fetch command line options
    parser = argparse.ArgumentParser(description="Generate POTCAR file based on elements listed in a POSCAR file.")
    parser.add_argument("--poscar", type=Path, default=Path("POSCAR"), help="Path to the POSCAR file.")
    parser.add_argument("--fetch-recommended", action="store_true", default=False, help="Fetch VASP recommended PAW potentials.")

    args = parser.parse_args()

    # Call POTCAR generator
    potcar_gen = PotcarGenerator()
    elements = potcar_gen.get_elements_from_poscar(args.poscar)
    potcar_gen.generate_potcar(elements, fetch_recommended=args.fetch_recommended)

if __name__ == "__main__":
    main()
