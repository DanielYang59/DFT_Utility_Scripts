#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from ase import Atoms
import numpy as np
import argparse
from ase.io import write

from .vacuumLayerManager import VacuumLayerManager
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

    def move_atoms_to_top(self):
        """
        Move atoms to the top of the cell.
        """
        z_coords = self.structure.positions[:, 2]
        min_z = min(z_coords)
        shift_value = self.structure.get_cell()[2, 2] - min_z
        self.structure.positions[:, 2] += shift_value

    def move_atoms_to_bottom(self):
        """
        Move atoms to the bottom of the cell.
        """
        z_coords = self.structure.positions[:, 2]
        max_z = max(z_coords)
        shift_value = max_z
        self.structure.positions[:, 2] -= shift_value

    def move_atoms_to_center(self):
        """
        Move the centroid of atoms to the center of the cell.
        """
        z_coords = self.structure.positions[:, 2]
        centroid = np.mean(z_coords)
        shift_value = self.structure.get_cell()[2, 2] / 2 - centroid
        self.structure.positions[:, 2] += shift_value

    def reposition_along_z(self, mode: str, check_vacuum_layer_numbers: bool = True):
        """
        Reposition atoms in the structure along the Z-axis based on the given mode.

        Parameters:
            mode (str): Specifies how atoms should be moved ("top", "bottom", "center", "centre").
            check_vacuum_layer_numbers (bool, optional): Whether to check for a single vacuum layer. Default is True.

        Raises:
            RuntimeError: If the mode is unsupported or if more than one vacuum layer is found when check_vacuum_layer_numbers is True.
        """
        # Check work mode
        if mode not in {"top", "bottom", "center", "centre"}:
            raise RuntimeError(f"Unsupported work mode {mode} for reposition module.")

        # Check vacuum layer count and position
        vacuum_manager = VacuumLayerManager(self.structure)
        vacuum_layer_count = vacuum_manager.count_vacuum_layer()
        vacuum_layer_position = vacuum_manager.locate_vacuum_layer()
        if check_vacuum_layer_numbers and vacuum_layer_count != 1:
            raise RuntimeError(f"Expect structure with exactly one vacuum layer, {vacuum_layer_count} found.")

        # Move atoms
        if mode == "top":
            self.move_atoms_to_top()
        elif mode == "bottom":
            self.move_atoms_to_bottom()
        else:
            self.move_atoms_to_center()

def main():
    """
    Main function to handle user input and execute atom repositioning.
    """
    parser = argparse.ArgumentParser(description="Reposition atoms in an ASE structure along the Z-axis.")
    parser.add_argument("mode", type=str, choices=["top", "bottom", "center", "centre"], help="How to reposition the atoms ('top', 'bottom', 'center', 'centre').")
    parser.add_argument("--check_vacuum_layer_number", default=True, type=bool, help="Check if there is only one vacuum layer. Default is True.")

    args = parser.parse_args()

    # Use find_or_request_poscar() to get the path to the POSCAR file.
    structure_path = find_or_request_poscar()

    # Read the structure using read_poscar() from utilities.
    structure = read_poscar(structure_path)

    repositioner = StructureRepositioner(structure)
    repositioner.reposition_along_z(mode=args.mode, check_vacuum_layer_numbers=args.check_vacuum_layer_number)

    # Save the modified structure to a file
    write(f'POSCAR_repositioned_{args.mode}', repositioner.structure, format='vasp')

if __name__ == "__main__":
    main()
