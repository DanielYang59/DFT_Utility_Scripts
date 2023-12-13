#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pathlib import Path
from typing import List
from ase import io
from ase.constraints import FixAtoms
import atexit

from .write_poscar import write_poscar

class PoscarAtomFixer:
    def __init__(self, poscarfile: Path) -> None:
        """
        Initialize the PoscarAtomFixer instance.

        Parameters:
            poscarfile (Path): Path to the POSCAR file.

        Raises:
            FileNotFoundError: If the specified POSCAR file is not found.

        Note:
            The PoscarAtomFixer instance is initialized with a POSCAR file, and an `atexit` handler is registered
            to call the `_write_modified_poscar` method with default output filename 'POSCAR_new' and overwrite set to True
            upon program exit.

        """
        if poscarfile.is_file():
            self.poscar = io.read(poscarfile)
        else:
            raise FileNotFoundError(f"Cannot found POSCAR file {poscarfile}.")

        # Write new POSCAR upon exiting
        atexit.register(write_poscar, self.poscar, file_path=Path("POSCAR_new"), overwrite=True)


    def _convert_position_range_to_absolute(self) -> List[float]:
        """
        Convert the specified position range to absolute coordinates based on the given mode.

        If the position mode starts with "f", the position range is interpreted as fractional coordinates
        and is converted to absolute coordinates using the cell parameters of the POSCAR file.

        If the position mode starts with "r", the position range is interpreted as relative coordinates
        with respect to existing atoms. The minimum and maximum coordinates along the specified axis
        are determined, and the relative position range is then converted to absolute coordinates
        based on these minimum and maximum coordinates.

        If the position mode is "absolute," the position range is returned without any processing.

        Returns:
            list: A list containing the converted absolute position range [min_absolute, max_absolute].

        Raises:
            RuntimeError: If an illegal position range mode is encountered.

        """
        # convert "fractional" position selection to "absolute"
        if self.position_mode.startswith("f"):
            cell_params = self.poscar.get_cell()[self.axis_index][self.axis_index]

            absolute_position_range = [
                self.position_range[0] * cell_params,
                self.position_range[1] * cell_params
                ]

        # Or convert "relative" position selection to "absolute"
        elif self.position_mode.startswith("r"):
            # Calculate the position of the atom with the smallest/largest coordinates
            coordinates = [atom[self.axis_index] for atom in self.poscar.get_positions()]
            min_coordinate, max_coordinate = min(coordinates), max(coordinates)

            absolute_position_range = [
                min_coordinate + self.position_range[0] * (max_coordinate - min_coordinate),
                min_coordinate + self.position_range[1] * (max_coordinate - min_coordinate)
            ]

        # Or return absolute position range without processing
        elif self.position_mode == "absolute":
            absolute_position_range = self.position_range

        else:
            raise RuntimeError(f"Illegal position range mode {self.position_mode}.")

        assert len(absolute_position_range) == 2 and (absolute_position_range[1] > absolute_position_range[0])
        return absolute_position_range


    def _select_atom_by_position(self, abs_position_range: List[float]) -> List[int]:
        """
        Select atoms whose coordinates along the specified axis fall within the given absolute position range.

        Parameters:
            abs_position_range (List[float]): The absolute position range [min_absolute, max_absolute].

        Returns:
            List[int]: A list of atom indices that satisfy the condition (0-indexed).

        Example:
            If abs_position_range is [1.0, 15.0] and the axis is "x", the method will return a list of
            indices for atoms whose x-coordinate falls within the range [1.0, 15.0].
        """
        # Select atoms within the specified absolute position range
        return [
            idx for idx, pos in enumerate(self.poscar.positions[:, self.axis_index])
            if abs_position_range[0] <= pos <= abs_position_range[1]
        ]


    def fix_atoms_by_index(self, atom_indexes: List[int], verbose: bool = True) -> None:
        """
        Fix specified atoms using selective dynamics.

        Parameters:
            atom_indexes (List[int]): List of integers representing 0-indexed indices indicating atoms to be fixed.

        Note:
            This method uses selective dynamics to fix the specified atoms in the POSCAR file.
        """
        # Check for integer values, non-negativity, and duplicates
        if any(not isinstance(idx, int) or idx < 0 for idx in atom_indexes):
            raise ValueError("All values in atom_indexes must be integers greater than or equal to zero.")

        if len(atom_indexes) != len(set(atom_indexes)):
            raise ValueError("Duplicate values in atom_indexes are not allowed.")

        assert atom_indexes, "Empty index list detected."

        # Apply selective dynamics using FixAtoms constraint
        # Reference: https://wiki.fysik.dtu.dk/ase/ase/constraints.html
        fix_atoms_constraint = FixAtoms(indices=atom_indexes)
        self.poscar.set_constraint(fix_atoms_constraint)

        if verbose:
            print(f"The following atoms would be fixed: {', '.join(map(str, [i+1 for i in atom_indexes]))}.")  # offset atom index by 1


    def fix_by_position(self, position_range: List[float], position_mode: str = "absolute", axis: str = "z") -> None:
        """
        Fix atoms based on their coordinates within a specified range along a given axis.

        Parameters:
            position_range (List[float, float]): Range of coordinates to fix atoms.
            position_mode (str, optional): Mode of the position range. Either "absolute" (default) or "fractional".
            axis (str, optional): The axis along which to check coordinates. Should be one of {"x", "y", "z"} (default is "z").

        Raises:
            AssertionError: If the input parameters violate the specified conditions.
            ValueError: If the axis is not one of {"x", "y", "z"}.

        Note:
            - The position_range should be a list of two floats representing the lower and upper bounds of the coordinate range.
            - If position_mode is "absolute", the coordinate range is given in absolute coordinates.
            - If position_mode is "fractional", the coordinate range is given in fractional coordinates, and it will be converted to absolute coordinates using the cell parameters.
            - The atoms whose coordinates fall within the specified range along the specified axis will be fixed.

        """
        # Check and convert axis selection
        self.axis = axis.lower()
        assert axis in {"x", "y", "z"}

        # Define axis index
        self.axis_index = {"x": 0, "y": 1, "z": 2}[self.axis]

        # Check position range selection
        assert len(position_range) == 2
        self.position_range = [float(i) for i in position_range]

        self.position_mode = position_mode.lower()
        if position_mode == "absolute":
            assert self.position_range[1] > self.position_range[0] >= 0
        elif position_mode in {"fractional", "relative"}:  # fractional or relative
            assert 1 >= self.position_range[1] > self.position_range[0] >= 0
        else:
            raise ValueError(f"Illegal position mode {position_mode}.")

        # Convert "fractional" and "relative" position ranges to "absolute"
        abs_position_range = self._convert_position_range_to_absolute()

        # Fix atoms by indexing
        self.fix_atoms_by_index(self._select_atom_by_position(abs_position_range))
