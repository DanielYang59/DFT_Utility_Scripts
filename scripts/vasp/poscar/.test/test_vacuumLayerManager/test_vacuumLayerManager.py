#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pytest
from pathlib import Path
from ase.lattice.hexagonal import Graphene
from ase.build import graphene
from ase.io import write
import numpy as np
import sys

# Update the path to include your custom VacuumLayerManager
script_dir = Path(__file__).resolve().parent
sys_path_to_append = script_dir.parents[5] / "Developer/DFT_Utility_Scripts/scripts/vasp/poscar"
sys.path.append(str(sys_path_to_append))

from vacuumLayerManager import VacuumLayerManager

@pytest.fixture
def sample_structure():
    """
    Fixture to provide a sample atomic structure for tests.
    """
    # Create a graphene unit cell
    atoms = Graphene(symbol='C', latticeconstant={'a': 2.46, 'c': 5.0})

    # Add a vacuum layer of 20 Ångströms along the z-axis
    atoms.cell[2][2] = 20.0

    test_path = Path("test_poscar")
    write(test_path, atoms, format="vasp")
    yield test_path
    test_path.unlink()

def test_count_vacuum_layers(sample_structure):
    """
    Test for counting the vacuum layers.
    """
    vacuum_setter = VacuumLayerManager(input_structure=sample_structure, axis="z")
    assert vacuum_setter.count_vacuum_layers() == 1

def test_adjust_vacuum_thickness(sample_structure):
    """
    Test for adjusting the vacuum thickness.
    """
    vacuum_setter = VacuumLayerManager(input_structure=sample_structure, axis="z")
    vacuum_setter.adjust_vacuum_thickness(new_vacuum=15.0)
    new_thickness = vacuum_setter.calculate_vacuum_thickness()
    assert new_thickness == 15.0

def rotate_atoms_and_cell(atoms, angle, axis):
    """
    Rotate both atoms and the cell manually.
    """
    atoms.rotate(angle, axis)

    angle_rad = np.radians(angle)
    if axis == 'x':
        rotation_matrix = np.array([[1, 0, 0],
                                    [0, np.cos(angle_rad), -np.sin(angle_rad)],
                                    [0, np.sin(angle_rad), np.cos(angle_rad)]])
    elif axis == 'y':
        rotation_matrix = np.array([[np.cos(angle_rad), 0, np.sin(angle_rad)],
                                    [0, 1, 0],
                                    [-np.sin(angle_rad), 0, np.cos(angle_rad)]])
    elif axis == 'z':
        rotation_matrix = np.array([[np.cos(angle_rad), -np.sin(angle_rad), 0],
                                    [np.sin(angle_rad), np.cos(angle_rad), 0],
                                    [0, 0, 1]])

    cell = atoms.get_cell()
    rotated_cell = np.dot(cell, rotation_matrix.T)
    atoms.set_cell(rotated_cell)

def test_adjust_vacuum_thickness_2D_structure_xyz():
    """
    Test for adjusting the vacuum thickness in a 2D graphene structure along z, x, and y axes.
    """
    # Create output directory if it doesn't exist
    output_dir = Path("test_output")
    output_dir.mkdir(exist_ok=True)

    initial_vacuum = 10.0  # 5.0 Angstrom on each side

    # Testing for z, x, and y axes
    for axis in ['z', 'x', 'y']:
        # Generate a 2D graphene structure
        atoms = graphene(size=(1, 1, 1), vacuum=5.0)

        # Rotate both atoms and cell if necessary
        if axis == 'x':
            rotate_atoms_and_cell(atoms, 90, 'y')
        elif axis == 'y':
            rotate_atoms_and_cell(atoms, 90, 'x')

        test_path_initial = output_dir / f"test_poscar_initial_{axis}"
        write(test_path_initial, atoms, format="vasp")

        # Check the initial vacuum thickness
        vacuum_setter = VacuumLayerManager(input_structure=test_path_initial, axis=axis)
        assert vacuum_setter.calculate_vacuum_thickness() == initial_vacuum

        # Adjust vacuum thickness and save the structure
        new_vacuum = 15.0  # 7.5 Angstrom on each side
        vacuum_setter.adjust_vacuum_thickness(new_vacuum=new_vacuum)
        test_path_modified = output_dir / f"test_poscar_modified_{axis}"
        write(test_path_modified, vacuum_setter.structure, format="vasp")

        # Check the new vacuum thickness
        assert vacuum_setter.calculate_vacuum_thickness() == new_vacuum

if __name__ == "__main__":
    pytest.main()
