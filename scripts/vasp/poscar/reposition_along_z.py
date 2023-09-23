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
    A utility class for manipulating the positions of atoms in an ASE Atoms object
    along the Z-axis. This class provides functionalities to reposition atoms,
    particularly in structures with or without a vacuum layer along the Z-axis.

    Attributes:
        structure (Atoms): The ASE Atoms object representing the structure
                           whose atoms are to be repositioned.

    Methods:
        __init__(self, structure: Atoms): Initialize the class.

        move_continuous_atoms(self, mode: str): Move atoms continuously based on
                                                the given mode ("top", "bottom", "center").

        move_split_atoms(self, mode: str): Reposition atoms that are split by a
                                           vacuum layer based on the given mode.

        reposition_along_z(self, mode: str): Perform atom repositioning based on
                                             the specified mode and vacuum layer presence.
    """

    def __init__(self, structure: Atoms):
        """
        Initialize the StructureRepositioner class with an ASE Atoms object.

        Parameters:
            structure (Atoms): The Atoms object representing the structure to be modified.
        """
        self.structure = structure

    def move_continuous_atoms(self, mode: str):
        """
        Move all atoms in the structure based on the specified mode along the Z-axis.

        Parameters:
            mode (str): Specifies where the atoms should be moved to.
                        Accepts one of the following: 'top', 'bottom', 'center', 'centre'.

        Raises:
            ValueError: If an unsupported mode is provided.
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
        Move atoms that are 'split' by a vacuum layer in the middle of the cell.
        In reality, the atoms are continuous due to the periodic boundary conditions.
        The method first joins the 'split' atoms by moving one part to the other,
        and then repositions them based on the mode.

        Parameters:
            mode (str): Specifies where the atoms should be moved to.
                        Accepts one of the following: 'top', 'bottom', 'center', 'centre'.
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
        Master function to reposition atoms based on the specified mode and
        the presence of a vacuum layer in the cell. It delegates the task to
        either `move_continuous_atoms` or `move_split_atoms` based on the
        vacuum layer position.

        Parameters:
            mode (str): Specifies where the atoms should be moved to.
                        Accepts one of the following: 'top', 'bottom', 'center', 'centre'.

        Raises:
            ValueError: If an unsupported mode is provided.
            RuntimeError: If more than one vacuum layers are present.
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
    Main function to parse command-line arguments and execute the repositioning
    of atoms in the structure. It reads the structure from a POSCAR file,
    performs the repositioning using the `StructureRepositioner` class,
    and writes the modified structure back to a new POSCAR file.
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
