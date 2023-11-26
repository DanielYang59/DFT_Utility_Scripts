#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pathlib import Path
from typing import List
import ase

class PoscarAtomFixer:
    def __init__(self, poscarfile: Path) -> None:
        if poscarfile.is_file():
            self.poscar = ase.io.read(poscarfile)
        else:
            raise FileNotFoundError(f"Cannot found POSCAR file {poscarfile}.")

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

    def fix_by_position(self, axis: str, ) -> None:
        axis = axis.lower()
        assert axis in {"x", "y", "z"}


    def fix_by_element(self, elements: List[str]) -> None:
        # Check if is legal element
        pass

        # Convert element to atom indexing

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

if __name__ == "__main__":
    pass
