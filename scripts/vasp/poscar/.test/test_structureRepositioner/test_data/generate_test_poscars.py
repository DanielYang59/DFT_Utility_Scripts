#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from ase.build import graphene
from ase.io import write
from pathlib import Path
import numpy as np

def generate_offset_graphene_with_vacuum(output_dir: Path, axis: str, vacuum: float = 10.0, offset: float = 2.0):
    """
    Generate a POSCAR file for a graphene structure with a vacuum layer,
    and with the graphene layer offset from the center along the specified axis.

    Parameters:
        output_dir (Path): The directory where the POSCAR file will be saved.
        axis (str): The axis along which the graphene will be offset and the vacuum will be applied ('x', 'y', 'z').
        vacuum (float): The size of the vacuum layer along the specified axis in Angstrom.
        offset (float): The offset from the center for the graphene layer along the specified axis in Angstrom.
    """
    # Create the output directory if it doesn't exist
    output_dir.mkdir(parents=True, exist_ok=True)

    # Create a graphene structure using ASE
    atoms = graphene()

    # Define axis index based on user input
    axis_index = {"x": 0, "y": 1, "z": 2}[axis]

    # Convert the 2D cell to a 3D cell
    cell = atoms.cell
    new_cell = np.eye(3)
    new_cell[0:2, 0:2] = cell[0:2, 0:2]
    new_cell[axis_index, axis_index] += vacuum
    atoms.set_cell(new_cell)

    # Center the atoms in the cell
    atoms.center()

    # Offset the graphene layer from the center along the specified axis
    atoms.positions[:, axis_index] += offset

    # Write the structure to a POSCAR file
    poscar_path = output_dir / f"POSCAR_graphene_offset_{axis}"
    write(poscar_path, atoms, format="vasp")

if __name__ == "__main__":
    output_dir = Path(".")
    for axis in ["x", "y", "z"]:
        generate_offset_graphene_with_vacuum(output_dir, axis)
