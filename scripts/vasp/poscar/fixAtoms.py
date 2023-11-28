#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pathlib import Path
from typing import List
from ase import io
from ase.constraints import FixAtoms
import atexit

from lib.write_poscar import write_poscar
from lib.interpret_atom_selection import interpret_atom_selection

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

    def _fix_atoms(self, atom_indexes: List[int]) -> None:
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
        fix_atoms_constraint = FixAtoms(indices=atom_indexes)  # ref: https://wiki.fysik.dtu.dk/ase/ase/constraints.html
        self.poscar.set_constraint(fix_atoms_constraint)

    def _convert_position_range_to_absolute(self):
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
        # Define axis index
        axis_index = {"x": 0, "y": 1, "z": 2}[self.axis]

        # convert "fractional" position selection to "absolute"
        if self.position_mode.startswith("f"):
            cell_params = self.poscar.get_cell()  # [len(a), len(b), len(c), angle(b,c), angle(a,c), angle(a,b)]

            return [
                self.position_range[0] * cell_params[axis_index],
                self.position_range[1] * cell_params[axis_index]
                ]

        # Or convert "relative" position selection to "absolute"
        elif self.position_mode.startswith("r"):
            # Calculate the position of the atom with the smallest/largest coordinates
            coordinates = [atom[axis_index] for atom in self.poscar.get_positions()]
            min_coordinate, max_coordinate = min(coordinates), max(coordinates)

            return [
                min_coordinate + self.position_range[0] * (max_coordinate - min_coordinate),
                min_coordinate + self.position_range[1] * (max_coordinate - min_coordinate)
            ]

        # Or return absolute position range without processing
        elif self.position_mode == "absolute":
            return self.position_range

        else:
            raise RuntimeError(f"Illegal position range mode {self.position_mode}.")

    def _select_atom_by_position(self, position_range: List[int]) -> List[int]:
        # DEBUG
        atom_indices = [
            idx for idx, pos in enumerate(self.poscar.positions[:, "xyz".index(axis)]) if position_range[0] <= pos <= position_range[1]
            ]

        return atom_indices

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

        # Check position range selection
        assert len(position_range) == 2
        self.position_range = [float(i) for i in position_range]

        self.position_mode = position_mode.lower()
        if position_mode.startswith("a"):  # absolute
            assert position_range[1] > position_range[0] >= 0
        else:  # fractional or relative
            assert 1 >= position_range[1] > position_range[0] >= 0

        # Convert "fractional" and "relative" position ranges to "absolute"
        abs_position_range = self._convert_position_range_to_absolute()

        # Fix atoms by indexing
        self._fix_atoms(self._select_atom_by_position(abs_position_range))

def main():
    # Select function from banner
    banner =\
    """
    -------------- POSCAR Atom Fixer -----------------
    Please selection a function by indexing:
    1. Fix atom by position range.
    2. Fix atom by elements/indexings.
    --------------------------------------------------
    """
    selected_function = input(banner)

    # Initialize POSCAR fixer
    poscarfile = Path.cwd() / "POSCAR"
    atom_list = io.read(poscarfile, format="vasp").get_chemical_symbols()
    fixer = PoscarAtomFixer(poscarfile=poscarfile)

    # Selection function
    if selected_function == "1":  # fix by position range
        position_range = input("Please input position range as [start-end]:")
        position_mode = input("Absolute, fractional or relative position?").lower()
        axis = input("Along which axis?").lower()
        fixer.fix_by_position(position_range.split("-"), position_mode, axis)

    elif selected_function == "2":  # fix by elements or indexes
        selection_banner = \
        """Please input element/index selection. Rules:
            - single indexing (one-indexed): "5"
            - indexing range:"1-3"
            - element: "Fe"
            - Combine above by ","
        """
        user_selection = input(selection_banner).split(",")

        indexings = interpret_atom_selection(atom_list=atom_list, index_selections=user_selection, indexing_mode="zero")
        fixer._fix_atoms(indexings)

    else:
        raise RuntimeError("Illegal function selection.")

    # Verbose
    print("New POSCAR written to \'POSCAR_new\'.")

if __name__ == "__main__":
    main()
