#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pathlib import Path
import re

def get_vasp_version(vasp_dir: Path) -> str:
    """
    Retrieve the VASP version from the first line of the OUTCAR file.

    Parameters:
        - vasp_dir (Path): The path to the directory containing the VASP OUTCAR file.

    Returns:
        - str: The extracted VASP version (e.g., "5.4.4").

    Raises:
        - FileNotFoundError: If the OUTCAR file is not found in the specified directory.
        - ValueError: If the VASP version is not found in the first line of the OUTCAR file.
    """
    outcar_path = vasp_dir / "OUTCAR"

    if not outcar_path.is_file():
        raise FileNotFoundError(f"OUTCAR file not found in {vasp_dir}")

    # Read the first line of the OUTCAR file
    with open(outcar_path, 'r') as outcar_file:
        first_line = outcar_file.readline()

    # Search for the VASP version in the first line
    version_match = re.search(r'\bvasp\.(\d+\.\d+\.\d+)\b', first_line, re.IGNORECASE)

    if version_match:
        return version_match.group(1)
    else:
        raise ValueError(f"VASP version not found in the first line of OUTCAR under {vasp_dir}.")

# Test area
if __name__ == "__main__":
    vasp_directory = Path(".")

    try:
        vasp_version = get_vasp_version(vasp_directory)
        print(f"VASP version: {vasp_version}")
    except Exception as e:
        print(f"Error: {e}")
