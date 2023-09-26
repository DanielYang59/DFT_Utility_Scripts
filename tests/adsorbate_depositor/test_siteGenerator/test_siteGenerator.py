#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pathlib import Path
import pytest
import SiteGenerator  # DEBUG
import numpy as np

@pytest.fixture
def sample_POSCAR_path():
    # This assumes you have a sample POSCAR file for testing in a folder named 'tests'
    return Path("tests/sample_POSCAR")

@pytest.fixture
def valid_site_generator(sample_POSCAR_path):
    return SiteGenerator(sample_POSCAR_path, 2.0, ["1", "2_3"])

def test_invalid_POSCAR():
    with pytest.raises(FileNotFoundError):
        SiteGenerator(Path("nonexistent_POSCAR"), 2.0, ["1"])

def test_invalid_distance_type(sample_POSCAR_path):
    with pytest.raises(TypeError):
        SiteGenerator(sample_POSCAR_path, "2.0", ["1"])

def test_negative_distance(sample_POSCAR_path):
    with pytest.raises(ValueError):
        SiteGenerator(sample_POSCAR_path, -2.0, ["1"])

def test_empty_sites(sample_POSCAR_path):
    with pytest.raises(ValueError):
        SiteGenerator(sample_POSCAR_path, 2.0, [])

def test_check_site(valid_site_generator):
    with pytest.raises(ValueError):
        valid_site_generator._check_site("100")  # Assuming 100 is not a valid site

def test_calculate_centroid(valid_site_generator):
    centroid = valid_site_generator._calculate_centroid([[0, 0, 0], [0, 2, 0], [2, 0, 0], [2, 2, 0]])
    np.testing.assert_almost_equal(centroid, [1, 1, 0])

def test_calculate_site(valid_site_generator):
    site_position = valid_site_generator._calculate_site("1")
    # TODO:
