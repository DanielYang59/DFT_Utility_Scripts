#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from ase import Atoms

def cartesian_to_direct(atoms):
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

def direct_to_cartesian(atoms):
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
