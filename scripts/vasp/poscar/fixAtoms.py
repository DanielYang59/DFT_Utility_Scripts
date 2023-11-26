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
        pass

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
        # One-indexing

        # Check for duplicates
        pass

if __name__ == "__main__":
    pass
