#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from ase import Atoms
import numpy as np
import argparse
from ase.io import write
from pathlib import Path
from vacuumLayerManager import VacuumLayerManager
from lib.utilities import find_or_request_poscar, read_poscar
import warnings

class StructureRepositioner:
    """
    A utility class for manipulating the positions of atoms in an ASE Atoms object.
    Supports repositioning along any specified axis ('x', 'y', 'z').

    Attributes:
        structure (Atoms): The Atoms object representing the structure to be modified.
        axis (str): The axis ('x', 'y', 'z') along which atoms will be repositioned.

    Methods:
        __init__(self, structure: Atoms, axis: str): Initializes the StructureRepositioner.
        move_continuous_atoms(self, mode: str): Move atoms continuously along the axis.
        move_split_atoms(self, mode: str): Reposition atoms split by a vacuum layer.
        reposition_along_axis(self, mode: str): Main method to perform atom repositioning.
    """

    def __init__(self, structure: Atoms, axis: str = "z"):
        """
        Initialize the class with the structure and axis.

        Parameters:
            structure (Atoms): The Atoms object to be modified.
            axis (str): The axis along which to reposition atoms ('x', 'y', 'z').
        """
        self.structure = structure
        self.axis = axis
        self.axis_index = {"x": 0, "y": 1, "z": 2}[self.axis]

    def move_continuous_atoms(self, mode: str):
        """
        Move atoms continuously along the axis based on the specified mode.

        Parameters:
            mode (str): Where to move the atoms ('top', 'bottom', 'center', 'centre').
        """
        coords = self.structure.positions[:, self.axis_index]
        cell_size = self.structure.get_cell()[self.axis_index, self.axis_index]
        centroid = np.mean(coords)

        if mode == "top":
            shift_value = cell_size - max(coords)
        elif mode == "bottom":
            shift_value = -min(coords)
        elif mode in {"center", "centre"}:
            shift_value = cell_size / 2 - centroid
        else:
            raise ValueError(f"Unsupported mode: {mode}")

        self.structure.positions[:, self.axis_index] += shift_value

    def move_split_atoms(self, mode: str):
        """
        Move atoms that are split by a vacuum layer along the axis.

        Parameters:
            mode (str): Where to move the atoms ('top', 'bottom', 'center', 'centre').
        """
        coords = self.structure.positions[:, self.axis_index]
        cell_size = self.structure.get_cell()[self.axis_index, self.axis_index]
        median_coord = np.median(coords)
        top_indices = np.where(coords > median_coord)[0]

        self.structure.positions[top_indices, self.axis_index] -= cell_size

        if mode == "top":
            shift_value = cell_size - min(coords)
        elif mode == "bottom":
            shift_value = max(coords)
        else:
            centroid = np.mean(coords)
            shift_value = cell_size / 2 - centroid

        self.structure.positions[:, self.axis_index] += shift_value

    def reposition_along_axis(self, mode: str):
        """
        Master function to reposition atoms based on the specified mode and
        the presence of a vacuum layer in the cell.

        Parameters:
            mode (str): Specifies where the atoms should be moved to.
                        Accepts one of the following: 'top', 'bottom', 'center', 'centre'.

        Raises:
            ValueError: If an unsupported mode is provided.
            RuntimeError: If more than one vacuum layers are present.
        """
        if mode not in {"top", "bottom", "center", "centre"}:
            raise ValueError(f"Unsupported work mode {mode}.")

        vacuum_manager = VacuumLayerManager(self.structure, axis=self.axis)
        vacuum_layer_position = vacuum_manager.locate_vacuum_layer()
        vacuum_layer_count = vacuum_manager.count_vacuum_layers()

        if vacuum_layer_count >= 2:
            raise RuntimeError("Atom repositioner cannot handle cases where there are more than one vacuum layers.")

        if vacuum_layer_position == "middle":
            warnings.warn("Find vacuum layer in the middle of the cell.")
            self.move_split_atoms(mode)
        else:
            self.move_continuous_atoms(mode)

def main():
    """
    Main function to handle command-line arguments and execute the atom repositioning.
    """
    parser = argparse.ArgumentParser(description="Reposition atoms in an ASE structure.")
    parser.add_argument("mode", type=str, choices=["top", "bottom", "center", "centre"], help="How to reposition the atoms.")
    parser.add_argument("--axis", type=str, default="z", choices=["x", "y", "z"], help="Along which axis to reposition atoms.")

    args = parser.parse_args()

    # Get and load POSCAR
    structure_path = find_or_request_poscar()
    structure = read_poscar(structure_path)

    # Call the reposition_along_axis method to perform the repositioning
    repositioner = StructureRepositioner(structure, axis=args.axis)
    repositioner.reposition_along_axis(mode=args.mode)

    # Write output POSCAR
    output_path = Path(f"POSCAR_repositioned_{args.mode}_{args.axis}")
    write(output_path, repositioner.structure, format="vasp")

if __name__ == "__main__":
    main()
