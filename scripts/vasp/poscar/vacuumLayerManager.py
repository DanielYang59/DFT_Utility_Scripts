#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# TODO: rectify naming of positions (top/bottom/middle)

from pathlib import Path
import numpy as np
import warnings
from typing import Union
from ase import Atoms
from ase.io import read

from structureRepositioner import StructureRepositioner
from lib import find_or_request_poscar, write_poscar

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
            raise ValueError("Vacuum level threshold should be greater than zero.")
        elif threshold < 5:
            warnings.warn(f"Small vacuum level threshold of {threshold} Å set. Make sure this is what you want.")

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
            tuple: (gap_bottom, gap_top), the bottom and top positions of the largest gap.
        """
        z_coords = np.sort(self.structure.positions[:, self.axis_index])
        gaps = np.diff(z_coords)
        max_gap_index = np.argmax(gaps)
        gap_bottom = z_coords[max_gap_index]
        gap_top = z_coords[max_gap_index] + gaps[max_gap_index]
        return gap_bottom, gap_top

    def locate_vacuum_layer(self, lower_threshold: float = 0.25, upper_threshold: float = 0.75, split_threshold: float = 1.0) -> str:
        """
        Locates the position of the single vacuum layer in the structure.

        Args:
            lower_threshold (float, optional): Lower threshold as a fraction of cell height to define the bottom region. Default is 0.25.
            upper_threshold (float, optional): Upper threshold as a fraction of cell height to define the top region. Default is 0.75.
            split_threshold (float, optional): Gap size in Å to consider as part of a split vacuum layer. Default is 2.0 Å.

        Notes:
            This method assumes that there is exactly one vacuum layer. In the case of z-axis, the vacuum can:
                1. Be entirely at the top.
                2. Be entirely at the bottom.
                3. Be positioned in the middle.
                4. Be split between the top and bottom.

        Returns:
            str: Position of the vacuum layer defined along the z-axis ('top', 'bottom', 'middle', 'split').

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

        # Find the index of the largest gap
        max_gap_index = np.argmax(gaps)

        # Calculate the top and bottom positions of the gap
        gap_bottom = coords[max_gap_index]
        gap_top = coords[max_gap_index + 1]

        # Get the cell dimension along the selected axis
        cell_dim = self.structure.get_cell().diagonal()[self.axis_index]

        # Identify gap at top and bottom ends
        top_gap = cell_dim - gap_top
        bottom_gap = gap_bottom

        # Check the position of the vacuum layer based on the largest gap
        if gap_top >= upper_threshold * cell_dim:
            return 'top'
        elif gap_bottom <= lower_threshold * cell_dim:
            return 'bottom'
        elif top_gap >= split_threshold and bottom_gap >= split_threshold:
            warnings.warn(f"Vacuum layer is split between the top and bottom. Top gap: {top_gap} Å, bottom gap: {bottom_gap} Å.")
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

        # Check the special case for periodic boundary conditions at the "top" and "bottom"
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
        positions = self.structure.get_positions()
        min_position = positions[:, self.axis_index].min()
        max_position = positions[:, self.axis_index].max()

        vacuum_layer_thickness = cell_dim - (max_position - min_position)

        # Warn if vacuum layer thickness is suspicious
        if vacuum_layer_thickness <= warn_lower_threshold:
            warnings.warn(f"The vacuum layer thickness along the selected axis is only {vacuum_layer_thickness} Å.")
        if vacuum_layer_thickness >= (cell_dim * warn_upper_ratio_threshold):
            warnings.warn("The vacuum layer thickness along the selected axis is very close to the cell dimension. Please double-check your structure.")

        assert vacuum_layer_thickness >= 0
        return vacuum_layer_thickness

    def adjust_vacuum_thickness(self, new_vacuum: float) -> None:
        """
        Adjust the vacuum thickness along the selected axis in the unit cell while repositioning atoms.

        This method performs the following steps:
        1. Checks the validity of the new vacuum thickness.
        2. Repositions atoms to the "bottom" of the cell.
        3. Adjusts the cell dimension to create the new vacuum thickness at the "top".
        4. Repositions atoms back to the center of the cell.

        Args:
            new_vacuum (float): The new thickness for the vacuum layer in Å.

        Returns:
            None: The method updates the internal Atoms object with the adjusted vacuum thickness.

        Raises:
            ValueError: If the new vacuum thickness is less than or equal to zero.

        Warnings:
            Issues a warning indicating that the vacuum layer has been adjusted and atoms have been recentered.
        """
        # Check new vacuum layer thickness
        if new_vacuum <= 0:
            raise ValueError("Vacuum layer thickness cannot be negative.")

        # Put atoms to the bottom
        atom_repositioner = StructureRepositioner(structure=self.structure, axis=self.axis)
        self.structure = atom_repositioner.reposition_along_axis(mode="bottom")

        # Apply new vacuum layer thickness to the top
        cell = self.structure.get_cell()
        max_position = self.structure.positions[:, self.axis_index].max()
        cell[self.axis_index, self.axis_index] = max_position + new_vacuum
        self.structure.set_cell(cell)

        # Move atoms back to the center
        atom_repositioner = StructureRepositioner(structure=self.structure, axis=self.axis)
        self.structure = atom_repositioner.reposition_along_axis(mode="center")
        warnings.warn(f"Vacuum layer would be adjusted. Atoms would be centered along {self.axis}-axis.")

def main():
    """
    The main function to execute the vacuum adjustment workflow.
    """
    input_poscar = find_or_request_poscar()  # Or provide an Atoms object

    # Allow user to specify axis
    axis_choice = input("Please enter the axis ('x', 'y', 'z') along which you want to adjust the vacuum layer: ")
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
    new_vacuum = float(input(f"Please enter the new vacuum thickness along the {axis_choice}-axis: "))
    vacuum_setter.adjust_vacuum_thickness(new_vacuum)

    # Write adjusted POSCAR
    write_poscar(vacuum_setter.structure, "POSCAR_vacuum_adjusted")

if __name__ == "__main__":
    main()
