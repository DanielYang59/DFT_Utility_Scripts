#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from src.utilities import find_or_request_poscar, read_poscar, write_poscar, discover_functions

# from src.fix_atoms import fix_atoms
# from src.remove_atoms import remove_atoms
# from src.replace_atoms import replace_atoms
# from src.adjust_vacuum import adjust_vacuum
from src.coordinate_system_transfer import cartesian_to_direct, direct_to_cartesian

def main():
    """
    Main function to run the POSCAR manipulation tool.
    """

    # Discover available functions
    module_list = [cartesian_to_direct, direct_to_cartesian]
    discover_functions(module_list)

    # Ask the user to choose a function to execute
    choice = input("Choose a function to execute by entering its name: ").strip()

    # Find or request the POSCAR file path
    file_path = find_or_request_poscar()

    # Read the POSCAR file into an ASE Atoms object
    atoms = read_poscar(file_path)

    # Dynamically execute the chosen function
    if choice in module_list:
        new_atoms = globals()[choice](atoms)
        print(f"Successfully executed {choice}.")

        # For demonstration purposes, let's assume you have a function to write Atoms back to POSCAR
        write_poscar(new_atoms)
    else:
        print("Invalid choice.")

if __name__ == "__main__":
    main()
