#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from pathlib import Path

def generate_potcar(potcar_lib: Path, elements: list, output_potcarfile: Path = Path("POTCAR")) -> None:
    """
    Generate a POTCAR file based on a list of elements.

    Parameters:
        potcar_lib (Path): A Path object representing the directory where the POTCAR library resides.
        elements (list): A list containing the chemical symbols of the elements.
        output_potcarfile (Path): A Path object for the output POTCAR file. Defaults to 'POTCAR' in the current directory.

    Raises:
        FileNotFoundError: If POTCAR for any of the specified elements is not found in the library.
    """
    # Initialize an empty string to store POTCAR data
    potcar_data = ""

    for element in elements:
        element_potcar_path = potcar_lib / element / "POTCAR"

        # Check if POTCAR file for the element exists
        if not element_potcar_path.is_file():
            raise FileNotFoundError(f"POTCAR for {element} not found in {potcar_lib}.")

        # Write output POTCAR file
        with element_potcar_path.open() as f:
            potcar_data += f.read()


    # Write the combined POTCAR data to the output path
    with output_potcarfile.open("w") as f:
        f.write(potcar_data)

def get_elements_from_poscar(poscarfile: Path) -> list:
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
    # Check if POSCAR file exists
    if not Path(poscarfile).is_file():
        raise FileNotFoundError(f"The POSCAR file {poscarfile} does not exist.")

    # Get the 6th line in POSCAR and split the line into element symbols
    with poscarfile.open() as f:
        lines = f.readlines()
    elements = lines[5].strip().split()

    if not elements:
        raise RuntimeError("The elements list is empty. Check your POSCAR file.")

    return elements

def get_potcar_library_path() -> Path:
    """
    Get the path to the POTCAR library from the environment variable.

    Returns:
        Path: Path to the POTCAR library.

    Raises:
        EnvironmentError: If the POTCAR_LIBRARY_PATH environment variable is not set.
        FileNotFoundError: If the path specified in the environment variable does not exist or is not a directory.
    """
    # Get environment variable for path to POTCAR library
    POTCAR_LIBRARY_PATH = os.environ.get("POTCAR_LIBRARY_PATH")

    # Throw error if env var is not set
    if POTCAR_LIBRARY_PATH is None:
        raise EnvironmentError(
            "The POTCAR_LIBRARY_PATH environment variable is not set. "
            "Please set this variable to the path of your POTCAR library. "
            "For example, you can add 'export POTCAR_LIBRARY_PATH=/path/to/your/potcar/library' "
            "to your shell configuration file (.bashrc, .zshrc, etc.)."
        )

    # Check if the path exists and is a directory
    potcar_path = Path(POTCAR_LIBRARY_PATH)

    if not potcar_path.is_dir():
        raise FileNotFoundError(
            f"The path specified in POTCAR_LIBRARY_PATH ({POTCAR_LIBRARY_PATH}) either does not exist "
            "or is not a directory. Please check the path and try again."
        )

    return potcar_path

def main(poscarfile="POSCAR") -> None:
    """
    Main function to create a POTCAR file based on elements listed in a POSCAR file.

    Parameters:
        poscarfile (Path): Path to the POSCAR file. Defaults to 'POSCAR' in the current directory.
    """
    # Read and check POTCAR library path from environment variable
    potcar_path = get_potcar_library_path()

    # Get list of elements from POSCAR
    elements = get_elements_from_poscar(poscarfile)

    # Generate new POTCAR
    generate_potcar(potcar_path, elements)

if __name__ == "__main__":
    main()
