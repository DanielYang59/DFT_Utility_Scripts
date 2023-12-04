#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pytest
from pathlib import Path
from ase import Atoms
from .....scripts.vasp.poscar.lib.read_poscar import read_poscar

@pytest.fixture
def setup_paths():
    """
    Setup fixture for paths to test POSCAR files.
    """
    current_script_dir = Path(__file__).parent  # Get the directory of the current script
    valid_poscar_path = current_script_dir / "test_data" / "POSCAR_valid"
    invalid_poscar_path = current_script_dir / "test_data" / "POSCAR_invalid"
    return valid_poscar_path, invalid_poscar_path

def test_read_valid_poscar(setup_paths):
    """
    Test that reading a valid POSCAR returns an Atoms object.
    """
    valid_poscar_path, _ = setup_paths
    atoms = read_poscar(valid_poscar_path)
    assert isinstance(atoms, Atoms)

def test_read_invalid_poscar(setup_paths):
    """
    Test that reading an invalid POSCAR raises a FileNotFoundError.
    """
    _, invalid_poscar_path = setup_paths
    with pytest.raises(FileNotFoundError):
        read_poscar(invalid_poscar_path)

def test_read_poscar_str_path(setup_paths):
    """
    Test that read_poscar can handle string paths.
    """
    valid_poscar_path, _ = setup_paths
    atoms = read_poscar(str(valid_poscar_path))
    assert isinstance(atoms, Atoms)

def test_read_poscar_path_object(setup_paths):
    """
    Test that read_poscar can handle Path objects.
    """
    valid_poscar_path, _ = setup_paths
    atoms = read_poscar(valid_poscar_path)
    assert isinstance(atoms, Atoms)
