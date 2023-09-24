#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from ase import Atoms
from lib import read_poscar, write_poscar, find_or_request_poscar

def cartesian_to_direct(atoms: Atoms) -> Atoms:
    """
    Convert Cartesian coordinates to Direct coordinates.

    Parameters:
        atoms (ase.Atoms): An ASE Atoms object with Cartesian coordinates

    Returns:
        ase.Atoms: A new Atoms object with Direct coordinates
    """
    # Get scaled positions (direct coordinates)
    scaled_positions = atoms.get_scaled_positions()

    # Create a new Atoms object with the scaled positions
    new_atoms = Atoms(symbols=atoms.get_chemical_symbols(),
                      scaled_positions=scaled_positions,
                      cell=atoms.get_cell(),
                      pbc=atoms.get_pbc())

    return new_atoms

def direct_to_cartesian(atoms: Atoms) -> Atoms:
    """
    Convert Direct coordinates to Cartesian coordinates.

    Parameters:
        atoms (ase.Atoms): An ASE Atoms object with Direct coordinates

    Returns:
        ase.Atoms: A new Atoms object with Cartesian coordinates
    """
    # Get Cartesian positions
    positions = atoms.get_positions()

    # Create a new Atoms object with the Cartesian positions
    new_atoms = Atoms(symbols=atoms.get_chemical_symbols(),
                      positions=positions,
                      cell=atoms.get_cell(),
                      pbc=atoms.get_pbc())

    return new_atoms

def main():
    """
    Main function to prompt user for choice of coordinate conversion,
    perform the conversion, and save the result to a new POSCAR file.
    """
    poscar_path = find_or_request_poscar()
    atoms = read_poscar(poscar_path)

    print("Select an operation:")
    print("1: Cartesian to Direct")
    print("2: Direct to Cartesian")
    choice = input("Enter the number corresponding to your choice: ")

    if choice == '1':
        new_atoms = cartesian_to_direct(atoms)
        output_filename = "POSCAR_direct"
    elif choice == '2':
        new_atoms = direct_to_cartesian(atoms)
        output_filename = "POSCAR_cartesian"
    else:
        print("Invalid choice. Exiting.")
        return

    output_path = poscar_path.parent / output_filename
    write_poscar(new_atoms, output_path)
    print(f"Operation completed. New POSCAR file saved as {output_path}")

if __name__ == "__main__":
    main()
