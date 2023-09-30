#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
from pathlib import Path
import warnings
from typing import List

def generate_kpoints(kpoints: List[int], mesh_type: str, lower_warn_threshold: int = 100) -> str:
    """
    Generate the contents of a VASP KPOINTS file based on the given arguments.

    Parameters:
        kpoints (list[int]): Three integers specifying subdivisions along reciprocal lattice vectors (a b c).
        mesh_type (str): Type of mesh ('g' for Gamma-centered, 'm' for Monkhorst-Pack).
        lower_warn_threshold (int, optional): Lower threshold for raise a too many kpoints warning.

    Returns:
        str: The contents of the KPOINTS file.

    Raises:
        ValueError: If the kpoints list does not contain exactly three integers.
        ValueError: If any k-point value is less than or equal to zero.
        UserWarning: If any k-point value is greater than 100.
    """
    # Check if the length of kpoints is exactly 3
    if len(kpoints) != 3:
        raise ValueError("The kpoints list must contain exactly three integers.")

    if any(k <= 0 for k in kpoints):
        raise ValueError("All k-point values must be integers greater than zero.")

    if any(k > lower_warn_threshold for k in kpoints):
        warnings.warn(f"The number of k-points along at least one axis is greater than {lower_warn_threshold}.")

    mesh_type_str = "Gamma-centered" if mesh_type == "g" else "Monkhorst-Pack"

    kpoints_content = (
        "Regular k-point mesh          ! Type of k-point grid\n"
        "0                              ! 0 -> determine number of k points automatically\n"
        f"{mesh_type_str}                     ! generate a {mesh_type_str} mesh\n"
        f"{kpoints[0]}  {kpoints[1]}  {kpoints[2]}         ! subdivisions N_1, N_2 and N_3 along the reciprocal lattice vectors\n"
        "0  0  0                         ! optional shift of the mesh (s_1, s_2, s_3)\n"
    )

    return kpoints_content

def main():
    """
    Generate a VASP KPOINTS file based on the given command-line arguments.
    """
    # Initialize argparse
    parser = argparse.ArgumentParser(description="Generate a regular KPOINTS file for VASP calculations.")

    # Positional arguments for k-points along the three axes
    parser.add_argument("kpoints", type=int, nargs=3, help="Three integers specifying subdivisions along reciprocal lattice vectors (a b c).")

    # Optional argument for mesh type
    parser.add_argument("-m", "--mesh", choices=["g", "m"], default="g", help="Type of mesh ('g' for Gamma-centered, 'm' for Monkhorst-Pack). Default is 'g'.")

    # Parse arguments
    args = parser.parse_args()

    # Generate KPOINTS file content
    kpoints_content = generate_kpoints(args.kpoints, args.mesh)

    # Save to a file
    kpoints_file_path = Path("KPOINTS")
    with kpoints_file_path.open("w", encoding="utf-8") as f:
        f.write(kpoints_content)

    print(f"KPOINTS file generated with {args.mesh} mesh and k-points: {args.kpoints}")

if __name__ == "__main__":
    main()
