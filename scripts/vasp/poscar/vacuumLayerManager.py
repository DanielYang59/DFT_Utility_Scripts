#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# TODO: test transformation along x/y axis
# TODO: "adjust vacuum layer thickness" method return Atoms object
# TODO: test non-parallel x/y cell vector warnings
# TODO: need best fixing for "negative vacuum layer thickness" in calculate_vacuum_thickness method

from pathlib import Path
import numpy as np
import warnings
from typing import Union
from ase import Atoms
from ase.io import read
from argparse import ArgumentParser

from .structureRepositioner import StructureRepositioner
from .lib import find_or_request_poscar, write_poscar

class VacuumLayerManager:
    """
    A class to manage and adjust the vacuum layer of a structure.

    The class provides utilities for counting, calculating, and adjusting the vacuum layer.

    Attributes:
        structure (ase.Atoms): The atomic structure managed by this object.
        threshold (float): The threshold to consider a gap along the axis as a vacuum layer.
        axis (str): The axis along which the vacuum layer is managed ('x', 'y', or 'z').
        init_vacuum_layer (float): Initial vacuum layer thickness along the axis.

    Methods:
        _find_largest_gap(): Finds the largest gap in z-coordinates among atoms.
        locate_vacuum_layer(): Locates the position of the vacuum layer in the structure.
        count_vacuum_layers(): Counts the vacuum layers.
        calculate_vacuum_thickness(): Calculates the thickness of the vacuum layer.
        adjust_vacuum_thickness(): Adjusts the vacuum thickness.
    """

    def __init__(self, input_structure: Union[Atoms, Path, str], threshold: float = 5.0, axis: str = "z") -> None:
        """
        Initialize the VacuumLayerManager with either an ASE Atoms object or a path to a POSCAR/CONTCAR file.

        Args:
            input_structure (ase.Atoms or pathlib.Path or str): An ASE Atoms object or the path to a POSCAR/CONTCAR file.
            threshold (float): the threshold to consider a gap along the axis as a vacuum layer (in Å).
            axis (str): The axis along which the vacuum layer will be managed ('x', 'y', or 'z').
        """
        # Check and load input structure
        if isinstance(input_structure, Atoms):
            self.structure = input_structure

        elif isinstance(input_structure, (Path, str)):
            input_structure = Path(input_structure)
            if input_structure.is_file():
                self.structure = read(input_structure, format="vasp")
            else:
                raise FileNotFoundError("Input structure file not found.")

        else:
            raise ValueError("Input structure must be either an ASE Atoms object or a Path to a POSCAR/CONTCAR file.")

        # Check vacuum layer threshold
        if threshold <= 0:
            raise ValueError("Vacuum layer threshold should be greater than zero.")
        elif threshold < 5:
            warnings.warn(f"Small vacuum layer threshold of {threshold} Å set. Make sure this is what you want.")

        self.threshold = threshold

        # Validation for axis
        if axis.lower() not in {"x", "y", "z"}:
            raise ValueError("Invalid axis. Must be 'x', 'y', or 'z'.")

        self.axis = axis.lower()
        self.axis_index = {"x": 0, "y": 1, "z": 2}[self.axis]

        # Calculate vacuum layer count
        self.vacuum_layer_count = self.count_vacuum_layers()

        # Calculate vacuum layer thickness
        self.init_vacuum_layer = self.calculate_vacuum_thickness()

    def _find_largest_gap(self) -> tuple:
        """
        Find the largest gap along selected axis among atoms.

        Returns:
            tuple: (min_bound, max_bound), the lower and upper bounds of the largest gap.
        """
        coords = np.sort(self.structure.positions[:, self.axis_index])
        gaps = np.diff(coords)
        max_gap_index = np.argmax(gaps)
        min_bound = coords[max_gap_index]
        max_bound = coords[max_gap_index] + gaps[max_gap_index]
        return min_bound, max_bound

    def locate_vacuum_layer(self, lower_threshold: float = 0.25, upper_threshold: float = 0.75, split_threshold: float = 1.0) -> str:
        """
        Locates the position of the single vacuum layer in the structure.

        Args:
            lower_threshold (float, optional): Lower threshold as a fraction of cell height to define the bottom region. Default is 0.25.
            upper_threshold (float, optional): Upper threshold as a fraction of cell height to define the top region. Default is 0.75.
            split_threshold (float, optional): Gap size in Å to consider as part of a split vacuum layer. Default is 2.0 Å.

        Notes:
            This method assumes that there is exactly one vacuum layer. In the case of z-axis, the vacuum can:
                1. Be entirely at the top (max_bound).
                2. Be entirely at the bottom (min_bound).
                3. Be positioned in the middle.
                4. Be split between the top(max_bound) and bottom(min_bound).

        Returns:
            str: Position of the vacuum layer defined along the z-axis ('max_bound', 'min_bound', 'middle', 'split').

        Raises:
            RuntimeError: If there is not exactly one vacuum layer.
        """
        # Check vacuum layer count
        if self.vacuum_layer_count != 1:
            raise RuntimeError("Locate vacuum layer method only works when there is exactly one vacuum layer.")

        # Sort the coordinates
        coords = np.sort(self.structure.positions[:, self.axis_index])

        # Calculate the gaps between adjacent atoms along the selected axis
        gaps = np.diff(coords)

        # Calculate the max_bound and min_bound positions of the gap
        min_bound, max_bound = self._find_largest_gap()

        # Get the cell dimension along the selected axis
        cell_dim = self.structure.get_cell().diagonal()[self.axis_index]

        # Identify gap at max_bound and min_bound ends
        max_gap = cell_dim - max_bound
        min_gap = min_bound

        if max_bound >= upper_threshold * cell_dim:
            return 'max_bound'
        elif min_bound <= lower_threshold * cell_dim:
            return 'min_bound'
        elif max_gap >= split_threshold and min_gap >= split_threshold:
            warnings.warn(f"Vacuum layer is split between the max_bound and min_bound. Max gap: {max_gap} Å, Min gap: {min_gap} Å.")
            return 'split'
        else:
            return 'middle'

    def count_vacuum_layers(self) -> int:
        """
        Count vacuum layer numbers along selected axis.

        Returns:
            int: total number of vacuum layers
        """
        # Extract coordinates and sort them
        coords = np.sort(self.structure.positions[:, self.axis_index])

        # Compute the gaps between adjacent coordinates
        gaps = np.diff(coords)

        # Identify the gaps that are larger than the threshold
        large_gaps = gaps > self.threshold

        # Check the special case for periodic boundary conditions at the "max_bound" and "min_bound"
        cell_dim = self.structure.get_cell().diagonal()[self.axis_index]
        if (coords[-1] - coords[0] + (cell_dim - coords[-1] + coords[0])) > self.threshold:
            large_gaps = np.append(large_gaps, True)

        # Count the number of large gaps (i.e., the number of vacuum layers)
        return np.sum(large_gaps)

    def calculate_vacuum_thickness(self, warn_lower_threshold: float = 2.0, warn_upper_ratio_threshold: float = 0.9) -> float:
        """
        Calculate the vacuum thickness along the selected axis in the unit cell.

        Returns:
            float: Thickness of the vacuum layer.
        """
        # Calculate vacuum layer thickness along the selected axis
        cell_dim = self.structure.get_cell().diagonal()[self.axis_index]

        # Determine max_bound and min_bound of the positions
        min_position = self.structure.positions[:, self.axis_index].min()
        max_position = self.structure.positions[:, self.axis_index].max()

        vacuum_layer_thickness = cell_dim - (max_position - min_position)
        if vacuum_layer_thickness < 0:
            warnings.warn("Negative vacuum layer thickness found (there might be atoms outside the cell). Proceed with caution")
            # TODO: need a better fix
            return 0  # return 0 so that following adjustment could proceed (otherwise would stop running)

        # Warn if vacuum layer thickness is suspicious
        if vacuum_layer_thickness <= warn_lower_threshold:
            warnings.warn(f"The vacuum layer thickness along the selected axis is only {vacuum_layer_thickness} Å.")
        if vacuum_layer_thickness >= (cell_dim * warn_upper_ratio_threshold):
            warnings.warn("The vacuum layer thickness along the selected axis is very close to the cell dimension. Please double-check your structure.")

        return vacuum_layer_thickness

    def adjust_vacuum_thickness(self, new_vacuum: float, vacuum_warning_threshold: float = 5.0) -> None:
        """
        Adjust the vacuum thickness along a specified axis in the unit cell while repositioning atoms.

        This method performs the following steps to adjust the vacuum thickness:
        1. Validates the new vacuum thickness.
        2. Repositions atoms to the "min_bound" of the unit cell.
        3. Modifies the cell dimension to create the new vacuum thickness at the "max_bound" of the unit cell.
        4. Repositions atoms back to the center of the unit cell.

        Args:
            new_vacuum (float): The desired thickness for the vacuum layer in Angstroms (Å).
                Must be greater than zero.
            vacuum_warning_threshold (float, optional): A threshold value for issuing a warning
                when the requested vacuum thickness is too small. Defaults to 5.0 Å.

        Returns:
            None: The function modifies the internal Atoms object to reflect the adjusted vacuum thickness.

        Raises:
            ValueError: Raised if the new vacuum thickness is less than or equal to zero.

        Warnings:
            - Issues a warning if the new vacuum thickness is less than or equal to the `vacuum_warning_threshold`.
            - Issues a warning after the vacuum layer and atoms have been successfully adjusted and re-centered.

        """
        # Check new vacuum layer thickness
        if new_vacuum < 0:
            raise ValueError("Vacuum layer thickness cannot be negative.")
        elif new_vacuum <= vacuum_warning_threshold:
            warnings.warn(f"Small vacuum thickness of {new_vacuum} Å requested.")

        # Put atoms to the min_bound
        atom_repositioner = StructureRepositioner(structure=self.structure, axis=self.axis)
        self.structure = atom_repositioner.reposition_along_axis(mode="min_bound")

        # Apply new vacuum layer thickness to the max_bound
        cell = self.structure.get_cell()
        max_position = self.structure.positions[:, self.axis_index].max()
        cell[self.axis_index, self.axis_index] = max_position + new_vacuum
        self.structure.set_cell(cell)

        # Move atoms back to the center
        atom_repositioner = StructureRepositioner(structure=self.structure, axis=self.axis)
        self.structure = atom_repositioner.reposition_along_axis(mode="center")
        warnings.warn(f"Vacuum layer would be adjusted. Atoms would be centered along {self.axis}-axis.")

def main(args):
    """
    The main function to execute the vacuum adjustment workflow.

    This function performs the following steps:
    1. Reads in the structure (e.g., POSCAR) or Atoms object.
    2. Validates the axis choice specified via command-line arguments.
    3. Initializes a VacuumLayerManager object based on the structure and axis.
    4. Checks the number of vacuum layers in the structure.
    5. Calculates the current vacuum layer thickness.
    6. Adjusts the vacuum layer thickness based on the command-line argument.
    7. Writes the adjusted structure to a new POSCAR file.

    Args:
        args (Namespace): A namespace containing the parsed command-line arguments.
            - axis (str): The axis ('x', 'y', 'z') along which to adjust the vacuum layer.
            - new_vacuum (float): The new vacuum thickness along the specified axis.

    Raises:
        ValueError: If the axis choice is invalid or if there are issues with the vacuum layers in the structure.

    Examples:
        This function is typically run via the command line as follows:
        python your_script.py -a x -n 10.0
    """
    input_poscar = find_or_request_poscar()  # Or provide an Atoms object

    axis_choice = args.axis
    if axis_choice not in ["x", "y", "z"]:
        raise ValueError("Invalid axis choice. Must be 'x', 'y', or 'z'.")

    vacuum_setter = VacuumLayerManager(input_poscar, axis=axis_choice)

    # Check vacuum layer
    vacuum_layer_count = vacuum_setter.count_vacuum_layers()
    if vacuum_layer_count >= 2:
        raise ValueError("The structure contains more than one vacuum layer, which is not allowed.")
    elif vacuum_layer_count == 0:
        raise ValueError("No vacuum layer found. Please check your structure.")

    # Calculate vacuum layer thickness
    vacuum_layer_thickness = vacuum_setter.calculate_vacuum_thickness()
    print(f"Current vacuum thickness along the {axis_choice}-axis is {vacuum_layer_thickness}.")

    # Adjust vacuum layer thickness
    new_vacuum = args.new_vacuum
    vacuum_setter.adjust_vacuum_thickness(new_vacuum)

    # Write adjusted POSCAR
    write_poscar(vacuum_setter.structure, "POSCAR_vacuum_adjusted")

if __name__ == "__main__":
    parser = ArgumentParser(description="A program to adjust the vacuum layer of a structure.")
    parser.add_argument("-a", "--axis", choices=["x", "y", "z"], required=True, help="The axis ('x', 'y', 'z') along which to adjust the vacuum layer.")
    parser.add_argument("-n", "--new_vacuum", type=float, required=True, help="The new vacuum thickness along the specified axis.")
    args = parser.parse_args()
    main(args)
