#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pytest
from pathlib import Path
from ase.lattice.hexagonal import Graphene
from ase.build import graphene
from ase.io import write
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

def test_adjust_vacuum_thickness_2D_structure():
    """
    Test for adjusting the vacuum thickness in a 2D graphene structure.
    """
    # Create output directory if it doesn't exist
    output_dir = Path("test_output")
    output_dir.mkdir(exist_ok=True)

    # Generate a 2D graphene structure
    atoms = graphene(size=(1, 1, 1), vacuum=5.0)
    initial_vacuum = 10.0
    test_path_initial = output_dir / "test_poscar_initial"
    write(test_path_initial, atoms, format="vasp")

    # Check the initial vacuum thickness
    vacuum_setter = VacuumLayerManager(input_structure=test_path_initial, axis="z")
    assert vacuum_setter.calculate_vacuum_thickness() == initial_vacuum

    # Adjust vacuum thickness and save the structure
    new_vacuum = 15.0
    vacuum_setter.adjust_vacuum_thickness(new_vacuum=new_vacuum)
    test_path_modified = output_dir / "test_poscar_modified"
    write(test_path_modified, vacuum_setter.structure, format="vasp")

    # Check the new vacuum thickness
    assert vacuum_setter.calculate_vacuum_thickness() == new_vacuum

if __name__ == "__main__":
    pytest.main()
