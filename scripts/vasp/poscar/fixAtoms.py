#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from pathlib import Path
from ase import io

from lib.interpret_atom_selection import interpret_atom_selection
from lib.poscarAtomFixer import PoscarAtomFixer


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

        indexings = interpret_atom_selection(
            atom_list=atom_list,
            index_selections=user_selection,
            indexing_mode="zero"
            )

        fixer.fix_atoms_by_index(indexings)

    else:
        raise RuntimeError("Illegal function selection.")

    # Verbose
    print("Done! New POSCAR written to \'POSCAR_new\'.")

if __name__ == "__main__":
    main()
