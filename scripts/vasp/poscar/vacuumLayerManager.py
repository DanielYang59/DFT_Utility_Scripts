#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# TODO: update class docstring to show available methods.

from pathlib import Path
import numpy as np
import warnings
from typing import Union
from ase import Atoms
from ase.io import read

from .reposition_along_z import reposition_along_z
from lib.utilities import find_or_request_poscar, write_poscar

class VacuumLayerManager:
    """
    A class to manage and adjust the vacuum layer of a structure.

    This class assumes that the vacuum layer is along the z-axis of the structure.
    It provides utilities for counting, calculating, and adjusting the vacuum layer.

    Attributes:
        structure (ase.Atoms): The atomic structure managed by this object.
        old_vacuum_layer (float): Initial vacuum layer thickness along the z-axis.
    """

    def __init__(self, input_structure: Union[Atoms, Path, str]) -> None:
        """
        Initialize the VacuumLayerSetter with either an ASE Atoms object or a path to a POSCAR/CONTCAR file.

        Args:
            input_structure (ase.Atoms or pathlib.Path or str): An ASE Atoms object or the path to a POSCAR/CONTCAR file.
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

        # Calculate vacuum layer thickness
        self.old_vacuum_layer = self.calculate_vacuum_thickness()

    def locate_vacuum_layer(self, lower_threshold: float = 0.25, upper_threshold: float = 0.75) -> str:
        """
        Locates the position of the single vacuum layer in the structure.

        This method assumes that there is exactly one vacuum layer.

        Returns:
            str: Position of the vacuum layer ('top', 'bottom', 'middle').
        """
        # Check vacuum layer count
        if self.count_vacuum_layers() != 1:
            raise RuntimeError("Locate vacuum layer method only works when there is exactly one vacuum layer.")

        warnings.warn(f"Locate vacuum layer method works reliably only when the vacuum layer resides at the top{upper_threshold}/bottom{lower_threshold} of the model, and might generate unreliable results for more complicated cases.")

        # Sort the z-coordinates
        z_coords = np.sort(self.structure.positions[:, 2])

        # Calculate the gaps between adjacent atoms along the z-axis
        gaps = np.diff(z_coords)

        # Find the index of the largest gap
        max_gap_index = np.argmax(gaps)

        # Calculate the top and bottom positions of the gap
        gap_bottom = z_coords[max_gap_index]
        gap_top = z_coords[max_gap_index] + gaps[max_gap_index]

        # Get the cell dimension along the z-axis
        cell_dim_z = self.structure.get_cell().diagonal()[2]

        # Check the position of the vacuum layer based on the largest gap
        if gap_top >= upper_threshold * cell_dim_z:
            return 'top'
        elif gap_bottom <= lower_threshold * cell_dim_z:
            return 'bottom'
        else:
            return 'middle'

    def count_vacuum_layers(self, threshold: Union[float, int] = 5.0) -> int:
        """
        Count vacuum layer numbers along z-axis.

        Args:
            threshold (Union[float, int]): the threshold to consider a gap along the z-axis as a vacuum layer (in Å).

        Returns:
            int: total number of vacuum layers
        """
        # Extract z-coordinates and sort them
        z_coords = np.sort(self.structure.positions[:, 2])

        # Compute the gaps between adjacent z-coordinates
        gaps = np.diff(z_coords)

        # Identify the gaps that are larger than the threshold
        large_gaps = gaps > threshold

        # Check the special case for periodic boundary conditions at the top and bottom
        cell_dim_z = self.structure.get_cell().diagonal()[2]
        if (z_coords[-1] - z_coords[0] + (cell_dim_z - z_coords[-1] + z_coords[0])) > threshold:
            large_gaps = np.append(large_gaps, True)

        # Count the number of large gaps (i.e., the number of vacuum layers)
        return np.sum(large_gaps)

    def calculate_vacuum_thickness(self, warn_lower_threshold: float = 2.0, warn_upper_ratio_threshold: float = 0.9) -> float:
        """
        Calculate the vacuum thickness along the z-axis in the unit cell.

        Returns:
            float: Thickness of the vacuum layer along the z-axis.
        """
        # Calculate vacuum layer thickness along z-axis
        cell_dim_z = self.structure.get_cell().diagonal()[2]
        positions = self.structure.get_positions()
        min_position_z = positions[:, 2].min()
        max_position_z = positions[:, 2].max()

        vacuum_layer_z = cell_dim_z - (max_position_z - min_position_z)

        # Warn if vacuum layer thickness is suspicious
        if vacuum_layer_z <= warn_lower_threshold:
            warnings.warn(f"The vacuum layer thickness along the z-axis is only {vacuum_layer_z} Å.")
        if vacuum_layer_z >= (cell_dim_z * warn_upper_ratio_threshold):
            warnings.warn("The vacuum layer thickness along the z-axis is very close to the cell dimension in z-axis. Please double-check your structure.")

        assert vacuum_layer_z >= 0
        return vacuum_layer_z

    def adjust_vacuum_thickness(self, new_vacuum: Union[float, int]) -> None:
        """
        Adjust the vacuum thickness along the z-axis in the unit cell while repositioning atoms.

        This method performs the following steps:
        1. Checks the validity of the new vacuum thickness.
        2. Repositions atoms to the bottom of the cell.
        3. Adjusts the z-axis cell dimension to create the new vacuum thickness at the top.
        4. Repositions atoms back to the center of the cell.

        Args:
            new_vacuum (Union[float, int]): The new thickness for the vacuum layer along the z-axis (in Å).

        Returns:
            None: The method updates the internal Atoms object with the adjusted vacuum thickness.

        Raises:
            ValueError: If the new vacuum thickness is less than or equal to zero.

        Warnings:
            Issues a warning indicating that the vacuum layer has been adjusted and atoms have been recentered along the z-axis.
        """
        # Check new vacuum layer thickness
        if new_vacuum <= 0:
            raise ValueError("Vacuum layer thickness cannot be negative.")

        # Put atoms to the bottom
        self.structure = reposition_along_z(self.structure, mode="bottom", check_vacuum_layer_number=True)

        # Apply new vacuum layer thickness to the top
        cell = self.structure.get_cell()
        max_position_z = self.structure.positions[:, 2].max()
        cell[2, 2] = max_position_z + new_vacuum
        self.structure.set_cell(cell)

        # Move atoms back to the center
        self.structure = reposition_along_z(self.structure, "center", True)
        warnings.warn("Vacuum layer would be adjusted. Atoms would be centered along z-axis.")

def main():
    """
    The main function to execute the vacuum adjustment workflow.
    """
    input_poscar = find_or_request_poscar()  # Or provide an Atoms object
    vacuum_setter = VacuumLayerSetter(input_poscar)

    # Check vacuum layer
    vacuum_layer_count = vacuum_setter.count_vacuum_layer()
    if vacuum_layer_count >= 2:
        raise ValueError("The structure contains more than one vacuum layer, which is not allowed.")
    elif vacuum_layer_count == 0:
        raise ValueError("No vacuum layer found. Please check your structure.")

    # Calculate vacuum layer thickness
    z_vacuum_thickness = vacuum_setter.calculate_vacuum_thickness()
    print(f"Current vacuum thickness along the z-axis is {z_vacuum_thickness}.")

    # Adjust vacuum layer thickness
    new_z_vacuum = float(input("Please enter the new vacuum thickness along the z-axis: "))
    vacuum_setter.adjust_vacuum_thickness(new_z_vacuum)

    # Write adjusted POSCAR
    write_poscar(vacuum_setter.structure, "POSCAR_vacuum_adjusted")

if __name__ == "__main__":
    main()
