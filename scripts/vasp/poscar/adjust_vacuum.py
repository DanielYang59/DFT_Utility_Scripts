#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import warnings

from lib.utilities import read_poscar, find_or_request_poscar, write_poscar

def calculate_z_vacuum_thickness(atoms):
    """
    Calculate the vacuum thickness along the z-axis in the unit cell.

    Parameters:
    atoms (ase.Atoms): An ASE Atoms object representing the unit cell.

    Returns:
    float: Thickness of the vacuum along the z-axis.

    Warning:
    1. This function assumes that the atoms are positioned at one end of the unit cell,
       and the other end is vacuum. It does not account for the case where there's a vacuum
       level in the middle of the atom cluster along the z-axis.
    2. If the vacuum level is too close to the cell thickness along the z-axis, it may
       indicate an error in the POSCAR file or the need for adjustment.
    """
    cell_dim_z = atoms.get_cell().diagonal()[2]
    positions = atoms.get_positions()
    min_position_z = positions[:, 2].min()
    max_position_z = positions[:, 2].max()

    vacuum_level_z = cell_dim_z - (max_position_z - min_position_z)

    # Warn user if vacuum level is too small (vacuum level might be in the middle of the cell)
    if vacuum_level_z <= 2.0:
        warnings.warn(f"The vacuum level thickness along the z-axis is {vacuum_level_z}. Please make sure the atoms are at the center of the cell.")

    # Warn user if vacuum level is close to the total thickness of the cell
    if vacuum_level_z >= (0.9 * cell_dim_z):
        warnings.warn("The vacuum level thickness along the z-axis is very close to the cell dimension. Please double-check your POSCAR file.")

    assert vacuum_level_z >= 0

    return vacuum_level_z

def adjust_z_vacuum_thickness(atoms, new_vacuum):
    """
    Adjust the vacuum thickness along the z-axis in the unit cell.

    Parameters:
    atoms (ase.Atoms): An ASE Atoms object representing the unit cell.
    new_vacuum (float): The new vacuum thickness along the z-axis.

    Returns:
    ase.Atoms: A new Atoms object with the adjusted vacuum thickness.

    Warning:
    This function assumes that the atoms are positioned at one end of the unit cell, and the other end is vacuum. It does not account for the case where there's a vacuum level in the middle of the atom cluster along the z-axis (i.e., discrete positions).
    """
    cell = atoms.get_cell()
    max_position_z = atoms.positions[:, 2].max()
    cell[2, 2] = max_position_z + new_vacuum  #DEBUG
    new_atoms = atoms.copy()
    new_atoms.set_cell(cell)

    return new_atoms

def main():
    # Read POSCAR
    poscar_original = read_poscar(find_or_request_poscar())

    # Check current vacuum level
    z_vacuum_thickness = calculate_z_vacuum_thickness(poscar_original)

    # Show current vacuum level and request new vacuum level from user
    print(f"Current vacuum thickness along the z-axis is {z_vacuum_thickness}.")
    new_z_vacuum = float(input("Please enter the new vacuum thickness along the z-axis: "))

    # Adjust vacuum level
    poscar_updated = adjust_z_vacuum_thickness(poscar_original, new_z_vacuum)

    # Write POSCAR
    write_poscar(poscar_updated, "POSCAR_vacuum_adjusted")

if __name__ == "__main__":
    main()
