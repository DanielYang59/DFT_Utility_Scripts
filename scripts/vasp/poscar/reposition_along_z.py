#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from ase import Atoms
import numpy as np
import argparse
from ase.io import write

from vacuumLayerManager import VacuumLayerManager
from lib.utilities import find_or_request_poscar, read_poscar

class StructureRepositioner:
    """
    A class for repositioning the atoms in a given ASE structure along the Z-axis.

    Attributes:
        structure (Atoms): The structure to be modified.
    """

    def __init__(self, structure: Atoms):
        """
        Initialize the StructureRepositioner class with an ASE Atoms object.

        Parameters:
            structure (Atoms): The Atoms object to be modified.
        """
        self.structure = structure

    def move_continuous_atoms(self, mode: str):
        """
        Move atoms that are continuous to the specified position ("top", "bottom", "center", "centre") in the cell.

        Parameters:
            mode (str): Specifies where atoms should be moved ("top", "bottom", "center", "centre").
        """
        z_coords = self.structure.positions[:, 2]
        cell_height = self.structure.get_cell()[2, 2]
        centroid = np.mean(z_coords)

        if mode == "top":
            shift_value = cell_height - max(z_coords)
        elif mode == "bottom":
            shift_value = -min(z_coords)
        elif mode in {"center", "centre"}:
            shift_value = cell_height / 2 - centroid
        else:
            raise ValueError(f"Unsupported mode: {mode}")

        self.structure.positions[:, 2] += shift_value

    def move_split_atoms(self, mode: str) -> None:
        """
        Move atoms that are "split" by the vacuum layer in the middle of the cell.
        In reality, it is continuous because of the periodic boundary conditions.

        Parameters:
            mode (str): Specifies where atoms should be moved ("top", "bottom", "center", "centre").
        """
        # Get atom z coordinates and cell height
        z_coords = self.structure.positions[:, 2]
        cell_height = self.structure.get_cell()[2, 2]

        # Separate the "top" and "bottom" atoms based on the median z-coordinate
        median_z = np.median(z_coords)
        top_indices = np.where(z_coords > median_z)[0]

        # Step 1: Move the "top" atoms to just below the "bottom" atoms
        self.structure.positions[top_indices, 2] -= cell_height

        # Re-calculate the z-coordinates for "joined" atoms
        z_coords = self.structure.positions[:, 2]

        # Step 2: Move these "joined" atoms based on the mode
        if mode == "top":
            min_z = min(z_coords)
            shift_value = cell_height - min_z
        elif mode == "bottom":
            max_z = max(z_coords)
            shift_value = max_z
        else:  # center or centre
            centroid = np.mean(z_coords)
            shift_value = cell_height / 2 - centroid

        self.structure.positions[:, 2] += shift_value

    def reposition_along_z(self, mode: str) -> None:
        """
        Reposition atoms based on the specified mode and the presence of a vacuum layer.

        Parameters:
            mode (str): Specifies where atoms should be moved ("top", "bottom", "center").
        """
        # Check work mode
        if mode not in {"top", "bottom", "center", "centre"}:
            raise ValueError(f"Unsupported work mode {mode}.")

        # Check vacuum layer position and count
        vacuum_manager = VacuumLayerManager(self.structure)
        vacuum_layer_position = vacuum_manager.locate_vacuum_layer()
        vacuum_layer_count = vacuum_manager.count_vacuum_layers()

        if vacuum_layer_count >= 2:
            raise RuntimeError("Atom repositioner cannot handle cases where there are more than one vacuum layers.")

        # Move atoms accordingly
        if vacuum_layer_position == "middle":
            self.move_split_atoms(mode)
        else:
            self.move_continuous_atoms(mode)

def main():
    """
    Main function to handle user input and execute atom repositioning.
    """
    parser = argparse.ArgumentParser(description="Reposition atoms in an ASE structure along the Z-axis.")
    parser.add_argument("mode", type=str, choices=["top", "bottom", "center", "centre"], help="How to reposition the atoms.")

    args = parser.parse_args()

    structure_path = find_or_request_poscar()
    structure = read_poscar(structure_path)

    repositioner = StructureRepositioner(structure)
    repositioner.reposition_along_z(mode=args.mode)

    write(f'POSCAR_repositioned_{args.mode}', repositioner.structure, format='vasp')

if __name__ == "__main__":
    main()
