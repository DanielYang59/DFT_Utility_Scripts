#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
from pathlib import Path
import warnings

def main():
    """
    Generate a VASP KPOINTS file based on the given command-line arguments.

    The user can specify the number of k-points along each of the three axes (a, b, c),
    and can optionally choose between a Gamma-centered and Monkhorst-Pack mesh type.
    """
    # Initialize argparse
    parser = argparse.ArgumentParser(description="Generate a regular KPOINTS file for VASP calculations.")

    # Positional arguments for k-points along the three axes
    parser.add_argument("kpoints", type=int, nargs=3, help="Three integers specifying subdivisions along reciprocal lattice vectors (a b c)")

    # Optional argument for mesh type
    parser.add_argument("-m", "--mesh", choices=["g", "m"], default="g", help="Type of mesh ('g' for Gamma-centered, 'm' for Monkhorst-Pack). Default is 'g'.")

    # Parse arguments
    args = parser.parse_args()

    # Check if k-points are greater than zero
    if any(k <= 0 for k in args.kpoints):
        raise ValueError("All k-point values must be integers greater than zero.")

    # Issue a warning if k-points along any axis are greater than 100
    if any(k > 100 for k in args.kpoints):
        warnings.warn("The number of k-points along at least one axis is greater than 100.")

    # Set mesh type
    mesh_type = "Gamma-centered" if args.mesh == "g" else "Monkhorst-Pack"

    # Generate KPOINTS file
    kpoints_file_path = Path("KPOINTS")

    with kpoints_file_path.open("w") as f:
        f.write("Regular k-point mesh          ! Type of k-point grid\n")
        f.write("0                              ! 0 -> determine number of k points automatically\n")
        f.write(f"{mesh_type}                     ! generate a {mesh_type} mesh\n")
        f.write(f"{args.kpoints[0]}  {args.kpoints[1]}  {args.kpoints[2]}         ! subdivisions N_1, N_2 and N_3 along the reciprocal lattice vectors\n")
        f.write("0  0  0                         ! optional shift of the mesh (s_1, s_2, s_3)\n")

    print(f"KPOINTS file generated with {mesh_type} mesh and k-points: {args.kpoints}")

if __name__ == "__main__":
    main()
