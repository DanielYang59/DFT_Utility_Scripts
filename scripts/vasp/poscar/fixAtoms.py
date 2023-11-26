#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pathlib import Path
from typing import List

class PoscarAtomFixer:
    def __init__(self, poscarfile: Path) -> None:
        if poscarfile.is_file():
            self.poscarfile = poscarfile
        else:
            raise FileNotFoundError(f"Cannot found POSCAR file {poscarfile}.")

    def _fix_atoms(self, atom_indexes: List[int]) -> None:
        pass

    def _write_modified_poscar(self, output_filename: Path, overwrite: bool = True) -> None:
        # TODO:
        # use this as a decorator
        pass

    def fix_by_position(self, axis: str, ) -> None:
        axis = axis.lower()
        assert axis in {"x", "y", "z"}


    def fix_by_element(self, elements: List[str]) -> None:
        # Check if is legal element
        pass

    def fix_by_indexing(self, indexings: List[int]) -> None:
        # One-indexing

        # Check for duplicates
        pass

if __name__ == "__main__":
    pass
