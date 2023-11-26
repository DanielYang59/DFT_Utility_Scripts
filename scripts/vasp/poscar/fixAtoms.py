#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pathlib import Path
from typing import List
import ase
import periodictable
import atexit

class PoscarAtomFixer:
    def __init__(self, poscarfile: Path) -> None:
        if poscarfile.is_file():
            self.poscar = ase.io.read(poscarfile)
        else:
            raise FileNotFoundError(f"Cannot found POSCAR file {poscarfile}.")

        # Call _write_modifed_poscar method upon exiting
        atexit.register(self._write_modified_poscar, output_filename='POSCAR_new', overwrite=True)

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

        # Apply selective dynamics using set_constraint
        selective_dyn = [[True, True, True] for _ in range(len(self.poscar))]
        for idx in atom_indexes:
            selective_dyn[idx] = [False, False, False]

        self.poscar.set_constraint(selective_dyn)

    def _write_modified_poscar(self, output_filename: Path, overwrite: bool = True) -> None:
        """
        Write the modified atomic structure to a VASP POSCAR file.

        Parameters:
            output_filename (Path): The path to the output POSCAR file.
            overwrite (bool, optional): If False and the file already exists, a FileExistsError is raised.
        Set to True to overwrite the existing file. Default is True.

        Raises:
            FileExistsError: If the specified file already exists and 'overwrite' is set to False.

        Note:
        This method writes the modified atomic structure to a VASP POSCAR file. It checks whether the
        specified output file already exists. If it does and 'overwrite' is set to False, a FileExistsError
        is raised. If 'overwrite' is True or the file does not exist, the method proceeds to write the file.

        """
        # Check if the file already exists
        if output_filename.exists() and not overwrite:
            raise FileExistsError(f"The file '{output_filename}' already exists. Set 'overwrite' to True to overwrite.")

        # Write the modified POSCAR file
        ase.io.write(output_filename, self.poscar, format="vasp")

    def fix_by_position(self, position_range: List[float, float], position_mode: str = "absolute", axis: str = "z") -> None:
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
        # Check position range selection
        assert position_mode in {"absolute", "fractional"}
        assert len(position_range) == 2
        if position_mode == "absolute":
            assert position_range[1] > position_range[0] >= 0
        else:
            assert 1 >= position_range[1] > position_range[0] >= 0

        # Check axis selection
        axis = axis.lower()
        assert axis in {"x", "y", "z"}

        # Convert fractional position range to absolute
        if position_mode == "fractional":
            cell_params = self.poscar.get_cell()
            position_range = [
                position_range[0] * cell_params[axis][axis],
                position_range[1] * cell_params[axis][axis]
                ]

        # Convert position range to atom indices
        atom_indices = [
            idx for idx, pos in enumerate(self.poscar.positions[:, "xyz".index(axis)]) if position_range[0] <= pos <= position_range[1]
            ]

        # Fix atoms by indexing
        self._fix_atoms(atom_indices)

    def fix_by_element(self, elements: List[str]) -> None:
        """
        Fix specified atoms by their chemical symbols.

        Parameters:
            elements (List[str]): List of chemical symbols indicating atoms to be fixed.

        Raises:
            ValueError: If any value is not a legal chemical symbol, not a string, or if there are duplicates.
        """
        # Check for legal chemical symbols
        valid_symbols = {element.symbol for element in periodictable.elements}

        if any(element not in valid_symbols for element in elements):
            raise ValueError("One or more values in the list are not legal chemical symbols.")

        # Check if every value is a string
        if any(not isinstance(element, str) for element in elements):
            raise ValueError("One or more values in the list are not strings.")

        # Check for duplicates
        if len(elements) != len(set(elements)):
            raise ValueError("Duplicate values are not allowed in the list.")

        # Convert elements to indexings
        atom_list = self.poscar.get_chemical_symbols()
        indexings = [index for index, element in enumerate(atom_list) if element in elements]

        # Fix atom by indexing
        self._fix_atoms(indexings)

    def fix_by_indexing(self, indexings: List[int]) -> None:
        """
        Update atomic positions based on specified indices.

        Parameters:
            indexings (List[int]): List of integers representing one-indexed indices
        indicating atoms to be modified.

        Raises:
            ValueError: If indices are not integers, not one-indexed (start from 1), or if there are duplicate indices.

        Note:
            This method checks that all elements in the `indexings` list are integers and that
            the indices are one-indexed (start from 1). It also ensures that there are no duplicate indices.

            After the checks, the method converts the indices to 0-indexing (compatible with Python
            list indexing) and calls the private method `_fix_atoms` to apply modifications based on the specified indices.
        """
         # Check for integer indices
        if any(not isinstance(idx, int) for idx in indexings):
            raise ValueError("Indices must be integers.")

        # Check for one-indexing
        if any(idx < 1 for idx in indexings):
            raise ValueError("Indices must be one-indexed (start from 1).")

        # Check for duplicates
        if len(indexings) != len(set(indexings)):
            raise ValueError("Duplicate indices are not allowed.")

        # Convert to 0-indexing and fix atoms
        self._fix_atoms([(i - 1) for i in indexings])

def main():
    pass

if __name__ == "__main__":
    main()
