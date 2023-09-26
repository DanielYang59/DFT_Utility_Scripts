#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pytest
import AdsorbateDepositor  # DEBUG
from ase import Atoms
from pathlib import Path

@pytest.fixture
def setup_atoms():
    # Create a mock ASE Atoms object
    atoms = Atoms('H2O', positions=[(0, 0, 0), (0, 0.757, 0.586), (0, -0.757, 0.586)])
    return atoms

@pytest.fixture
def depositor(setup_atoms):
    return AdsorbateDepositor(setup_atoms)  # Assuming your class takes an Atoms object as an argument during instantiation

def test_reset_vacuum_layer_thickness(depositor, setup_atoms):
    modified_atoms = depositor._reset_vacuum_layer_thickness(setup_atoms, 10.0)
    # Add your assertions here to validate the behavior
    # For example: check the vacuum layer thickness in 'modified_atoms'

def test_write(depositor):
    output_dir = Path("./test_output")
    atoms_dict = {"test_adsorbate": Atoms('H2O', positions=[(0, 0, 0), (0, 0.757, 0.586), (0, -0.757, 0.586)])}
    depositor.write(atoms_dict, output_dir)
    assert (output_dir / "test_adsorbate/POSCAR_generated").exists()
    # Cleanup
    if output_dir.is_dir():
        # remove created files and directories
        pass  # implement cleanup

def test_deposit(depositor):
    results = depositor.deposit()
    # Add your assertions to validate the deposition process # DEBUG
    # For example: check the number of atoms in the 'results' dictionary
