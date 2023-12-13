#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from ase.io import read
from ase.io.vasp import write_vasp
from pathlib import Path

from lib.find_or_request_poscar import find_or_request_poscar


def detect_coordinate_system(poscar_path: Path) -> str:
    """
    Detect the coordinate system (Direct or Cartesian) from a POSCAR file.

    Parameters:
        poscar_path (Path): Path to the POSCAR file.

    Returns:
        str: "direct" or "cartesian" based on the detected coordinate system.
    """
    with open(poscar_path, 'r') as f:
        # Skip the first 7 lines
        for _ in range(7):
            next(f)

        # Read the 8th line of the POSCAR file
        line_8 = next(f).lower().strip()

        # Check if the line starts with "s" for selective dynamics
        if line_8.startswith("s"):
            # Read the 9th line of the POSCAR file
            line_9 = next(f).lower().strip()

            # Check if the 9th line contains an indicator for coordinate system
            if line_9.startswith("d"):
                coordinate_system = "direct"
            elif line_9.startswith("c"):
                coordinate_system = "cartesian"

        else:
            # Check if the 8th line contains an indicator for coordinate system
            if line_8.startswith("d"):
                coordinate_system = "direct"
            elif line_8.startswith("c"):
                coordinate_system = "cartesian"

    assert coordinate_system in {"direct", "cartesian"}
    return coordinate_system


def coordinate_system_transfer(verbose: bool = True):
    """
    Main function to prompt user for choice of coordinate conversion,
    perform the conversion, and save the result to a new POSCAR file.
    """
    # Import POSCAR
    poscar_path = find_or_request_poscar()
    atoms = read(poscar_path, format="vasp")


    # Detect current coordinate system
    current_coordinate_system = detect_coordinate_system(poscar_path)
    if verbose:
        print(f"Current coordinate system is: {current_coordinate_system}.")


    # Perform coordinate system transfer
    if current_coordinate_system == 'cartesian':  # cartesian to direct transfer
        output_filename = "POSCAR_direct"
        write_vasp(atoms=atoms, direct=True, file=output_filename)

    elif current_coordinate_system == 'direct':  # direct to cartesian transfer
        output_filename = "POSCAR_cartesian"
        write_vasp(atoms=atoms, direct=False, file=output_filename)

    else:
        raise RuntimeError(f"Invalid coordinate system {current_coordinate_system}.")


    # Verbose
    if verbose:
        print(f"Operation completed. New POSCAR file saved as {output_filename}")


if __name__ == "__main__":
    coordinate_system_transfer()
