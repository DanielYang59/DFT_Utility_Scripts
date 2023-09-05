#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import argparse
from pathlib import Path


def main():
    """
    Generate a VASP KPOINTS file based on the given command-line arguments.

    The user can specify the number of k-points along each of the three axes (a, b, c),
    and can optionally choose between a Gamma-centered or Monkhorst-Pack mesh type.

    Examples:
    ---------
    Generate a Gamma-centered mesh with 4 k-points along each axis:
    python3 kpoints.py 4 4 4

    Generate a Monkhorst-Pack mesh with 4 k-points along each axis:
    python3 kpoints.py 4 4 4 -m Monkhorst-Pack
    """
    # Initialize argparse
    parser = argparse.ArgumentParser(description="Generate a regular KPOINTS file for VASP calculations.")


    # Positional arguments for k-points along the three axes
    parser.add_argument("a", type=int, help="Number of subdivisions along the first reciprocal lattice vector")
    parser.add_argument("b", type=int, help="Number of subdivisions along the second reciprocal lattice vector")
    parser.add_argument("c", type=int, help="Number of subdivisions along the third reciprocal lattice vector")


    # Optional argument for mesh type
    parser.add_argument("-m", "--mesh", choices=["gamma", "Monkhorst-Pack"], default="gamma", help="Type of mesh. Default is Gamma-centered.")


    # Parse arguments
    args = parser.parse_args()


    # Check if k-points along each axis are greater than zero
    if args.a <= 0 or args.b <= 0 or args.c <= 0:
        raise ValueError("The number of k-points along each axis should be greater than zero.")


    # Set mesh type
    mesh_type = "Gamma" if args.mesh == "gamma" else "Monkhorst-Pack"


    # Generate KPOINTS file
    kpoints_list = [args.a, args.b, args.c]
    kpoints_file_path = Path("KPOINTS")

    with kpoints_file_path.open("w") as f:
        f.write("Regular k-point mesh\n")
        f.write("0\n")
        f.write(f"{mesh_type}\n")
        f.write(f"{kpoints_list[0]}  {kpoints_list[1]}  {kpoints_list[2]}\n")
        f.write("0  0  0\n")

    print(f"KPOINTS file generated with {mesh_type}-centered mesh and k-points: {kpoints_list}")


if __name__ == "__main__":
    main()
