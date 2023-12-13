#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# TODO: add vacuum layer detection (fix circular import with VacuumLayerManager)
# TODO: test generate warning for non-parallel cell sizes


import numpy as np
import argparse
from ase import Atoms
from ase.io import write, read
from pathlib import Path
import warnings

from .lib.find_or_request_poscar import find_or_request_poscar


class StructureRepositioner:
    """
    A utility class for manipulating the positions of atoms in an ASE Atoms object.

    The class allows for repositioning of atoms along a specified axis ('x', 'y', 'z') and offers various modes for repositioning.
    Before proceeding with the repositioning, it checks the alignment of the cell vector corresponding to the moving direction with
    the given axis and raises a warning if it's not aligned.

    Modes:
        - 'max_bound': Moves atoms towards the maximum boundary of the cell along the specified axis.
        - 'min_bound': Moves atoms towards the minimum boundary of the cell along the specified axis.
        - 'center' or 'centre': Moves atoms towards the center of the cell along the specified axis.

    Attributes:
        structure (Atoms): The Atoms object representing the structure to be modified.
        axis (str): The axis ('x', 'y', 'z') along which atoms will be repositioned.
        axis_index (int): The index representing the axis (0 for 'x', 1 for 'y', 2 for 'z').

    Methods:
        __init__(self, structure: Atoms, axis: str): Initializes the StructureRepositioner and checks cell vector alignment.
        _check_cell(self): Checks the alignment of the cell vector with the given direction and raises a warning if misaligned.
        _move_continuous_atoms(self, mode: str): Moves atoms continuously along the axis.
        # TODO: _move_split_atoms(self, mode: str): Repositions atoms that are split by a vacuum layer.
        reposition_along_axis(self, mode: str): Main method to perform atom repositioning.
    """

    def __init__(self, structure: Atoms, axis: str = "z") -> None:
        """
        Initialize the class with the structure and axis.

        Parameters:
            structure (Atoms): The Atoms object to be modified.
            axis (str): The axis along which to reposition atoms ('x', 'y', 'z').
        """
        if axis.lower() not in {"x", "y", "z"}:
            raise ValueError("Invalid axis. Must be 'x', 'y', or 'z'.")

        self.structure = structure
        self.cell = self.structure.get_cell()
        self.axis = axis.lower()
        self.axis_index = {"x": 0, "y": 1, "z": 2}[self.axis]

        # Check cell vector
        self._check_cell()

    def _check_cell(self) -> None:
        """Check the alignment of the cell vectors with the given direction.

        Raises:
            Warning: If the cell vector corresponding to the moving direction is not parallel to that direction.
        """
        cell_vector = self.cell[self.axis_index]

        # Check if only one component exists in the vector, meaning it is parallel to the axis.
        non_zero_count = np.count_nonzero(cell_vector)

        if non_zero_count != 1:
            warnings.warn(f"The cell vector along the {self.axis} axis is not parallel to the {self.axis}-axis. Proceed with caution.")

    def _move_continuous_atoms(self, mode: str) -> None:
        """
        Move atoms continuously along the axis based on the specified mode.

        Parameters:
            mode (str): Where to move the atoms. Accepts one of the following values:
                        - 'max_bound': Moves atoms towards the maximum boundary of the cell along the axis.
                        - 'min_bound': Moves atoms towards the minimum boundary of the cell along the axis.
                        - 'center' or 'centre': Moves atoms towards the center of the cell along the axis.

        Raises:
            ValueError: If an unsupported mode is provided.
        """
        coords = self.structure.positions[:, self.axis_index]
        cell_size = self.structure.get_cell()[self.axis_index, self.axis_index]
        centroid = np.mean(coords)

        if mode == "max_bound":
            shift_value = cell_size - max(coords)
        elif mode == "min_bound":
            shift_value = -min(coords)
        elif mode in {"center", "centre"}:
            shift_value = cell_size / 2 - centroid
        else:
            raise ValueError(f"Unsupported mode: {mode}")

        self.structure.positions[:, self.axis_index] += shift_value

    def _move_split_atoms(self, mode: str) -> None:
        """
        Move atoms that are split by a vacuum layer along the axis.

        Parameters:
            mode (str): Where to move the atoms. Accepts one of the following values:
                        - 'max_bound': Moves atoms towards the maximum boundary of the cell along the axis.
                        - 'min_bound': Moves atoms towards the minimum boundary of the cell along the axis.
                        - 'center' or 'centre': Moves atoms towards the center of the cell along the axis.

        Raises:
            ValueError: If an unsupported mode is provided.
        """
        coords = self.structure.positions[:, self.axis_index]
        cell_size = self.structure.get_cell()[self.axis_index, self.axis_index]
        median_coord = np.median(coords)
        max_indices = np.where(coords > median_coord)[0]

        self.structure.positions[max_indices, self.axis_index] -= cell_size

        if mode == "max_bound":
            shift_value = cell_size - min(coords)
        elif mode == "min_bound":
            shift_value = max(coords)
        else:
            centroid = np.mean(coords)
            shift_value = cell_size / 2 - centroid

        self.structure.positions[:, self.axis_index] += shift_value

    def reposition_along_axis(self, mode: str) -> Atoms:
        """
        Master function to reposition atoms based on the specified mode and
        the presence of a vacuum layer in the cell.

        Parameters:
            mode (str): Specifies where the atoms should be moved to. Accepts one of the following values:
                        - 'max_bound': Moves atoms towards the maximum boundary of the cell along the axis.
                        - 'min_bound': Moves atoms towards the minimum boundary of the cell along the axis.
                        - 'center' or 'centre': Moves atoms towards the center of the cell along the axis.

        Raises:
            ValueError: If an unsupported mode is provided.
            RuntimeError: If more than one vacuum layers are present.
        """
        if mode not in {"max_bound", "min_bound", "center", "centre"}:
            raise ValueError(f"Unsupported work mode {mode}.")

        # Move atoms
        # Issue a warning that the method only supports cases where atoms are continuous
        warnings.warn("This method currently only supports cases where atoms are continuous. It is not fully implemented yet.")
        self._move_continuous_atoms(mode)

        return self.structure

def main():
    """
    This script is designed for repositioning atoms in a given ASE-compatible structure
    (usually read from a POSCAR file). The repositioning can be done along a specific axis and
    in a certain mode, which could be either moving atoms to the maximum boundary, minimum boundary,
    or centering them along the specified axis.

    Command-Line Arguments:
        mode: Specifies how to reposition the atoms.
            Options: "max_bound", "min_bound", "center", "centre"
            Example: --mode max_bound

        axis: Specifies along which axis (x, y, z) the atoms should be repositioned.
            Options: "x", "y", "z"
            Default: "z"
            Example: --axis z

    Examples:
        Reposition atoms along the z-axis to the maximum boundary:
        $ python script_name.py max_bound --axis z

        Reposition atoms along the x-axis to the center:
        $ python script_name.py center --axis x

    Workflow:
        1. Parse the command-line arguments.
        2. Find or request the location of the POSCAR file to be read.
        3. Load the structure from the POSCAR file using the ASE library.
        4. Create an instance of the StructureRepositioner class with the loaded structure and specified axis.
        5. Call the reposition_along_axis method to perform the repositioning based on the mode.
        6. Write the repositioned structure to a new POSCAR file.
    """
    parser = argparse.ArgumentParser(description="Reposition atoms in an ASE structure.")
    parser.add_argument("mode", type=str, choices=["max_bound", "min_bound", "center", "centre"], help="How to reposition the atoms.")
    parser.add_argument("--axis", type=str, default="z", choices=["x", "y", "z"], help="Along which axis to reposition atoms.")

    args = parser.parse_args()

    # Get and load POSCAR
    structure_path = find_or_request_poscar()
    structure = read(structure_path, format="vasp")

    # Call the reposition_along_axis method to perform the repositioning
    repositioner = StructureRepositioner(structure, axis=args.axis)
    repositioner.reposition_along_axis(mode=args.mode)

    # Write output POSCAR
    output_path = Path(f"POSCAR_repositioned_{args.mode}_{args.axis}")
    write(output_path, repositioner.structure, format="vasp")

if __name__ == "__main__":
    main()
