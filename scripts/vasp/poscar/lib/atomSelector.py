#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pathlib import Path
from ase import io
from typing import List

class AtomSelector:
    def __init__(self, poscarfile: Path) -> None:
        # Check and read POSCAR
        if not poscarfile.is_file():
            raise FileNotFoundError(f"POSCAR file {poscarfile} not found.")
        self.poscar = io.read(poscarfile, format="vasp")

        self.atom_list = self.poscar.get_chemical_symbols()

    def interpret(self, index_selections: List[str], indexing_mode: str = "one") -> List[int]:
        """
        Converts user-specified atom selections into corresponding indexes in the atomic structure.

        Parameters:
        - index_selections (List[str]): A list of strings representing atom selections. Each string can be:
            - Single atom selection: "1"
            - Range selection: "1-3"
            - Element selection: "Fe"
        - indexing_mode (str, optional): The indexing mode to use, either "zero" or "one". Defaults to "one".

        Returns:
        - List[int]: A list of indexes corresponding to the selected atoms in the atomic structure.

        Raises:
        - ValueError: If no match is found for the specified atom selections.
        - AssertionError: If duplicate atom selections are detected.
        - RuntimeError: If an illegal indexing mode is provided.

        Note:
        - The function interprets user-specified atom selections and returns corresponding indexes.
        - Atom selections can be specified as single atoms, ranges, or chemical element symbols.
        - The indexing mode determines whether indexes start from zero or one.
        - Duplicate atom selections are not allowed.
        """
        indexings = []

        for selection in index_selections:
            # Single atom selection: "1"
            if selection.isdigit():
                indexings.append(int(selection))

            # Range selection: "1-3"
            elif "-" in selection:
                start, end = map(int, selection.split('-'))
                indexings.extend(list(range(start, end + 1)))

            # Element selection: "Fe"
            else:
                indexings.extend([(index + 1) for index, value in enumerate(self.atom_list) if value == selection])

        # Check atom selections
        assert len(indexings) == len(set(indexings)), "Duplicate atom selections detected."

        if not indexings:
            raise ValueError(f"No match found for atom request: {indexings}.")

        # Return indexings
        if indexing_mode == "zero":
            return indexings

        elif indexing_mode == "one":
            return [(i + 1) for i in indexings]

        else:
            raise RuntimeError("Illegal indexing mode (either zero or one).")
