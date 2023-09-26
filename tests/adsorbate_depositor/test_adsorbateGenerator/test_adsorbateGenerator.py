#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
from pathlib import Path
from ase import Atoms
import AdsorbateGenerator  # DEBUG

class TestAdsorbateGenerator(unittest.TestCase):

    def setUp(self):
        self.test_poscar_path = Path("path/to/test/POSCAR")  # Replace with your test POSCAR path
        self.test_database_path = Path("path/to/test/database")  # Replace with your test database path
        self.poscar_generator = AdsorbateGenerator("POSCAR", self.test_poscar_path)
        self.database_generator = AdsorbateGenerator("DATABASE", self.test_database_path)

    def test_extract_atoms(self):
        # Assuming you have a sample POSCAR in `self.test_poscar_path`
        atoms = self.poscar_generator._extract_atoms(self.test_poscar_path, [1, 2])
        self.assertIsInstance(atoms, Atoms)
        # More checks based on what you expect

    def test_generate_rotations(self):
        atoms = Atoms("H2", [(0, 0, 0), (1, 0, 0)])
        rotated = self.poscar_generator._generate_rotations(atoms)
        self.assertIsInstance(rotated, list)
        # More checks based on what you expect

    def test_generate_rotated_adsorbate_dict(self):
        adsorbate_dict = {"adsorbate": Atoms("H2", [(0, 0, 0), (1, 0, 0)])}
        rotated_dict = self.poscar_generator._generate_rotated_adsorbate_dict(adsorbate_dict)
        self.assertIsInstance(rotated_dict, dict)
        # More checks based on what you expect

    def test_load_adsorbate_from_database_header(self):
        adsorbate_dict = self.database_generator._load_adsorbate_from_database_header()
        self.assertIsInstance(adsorbate_dict, dict)
        # More checks based on what you expect

    def test_generate_adsorbates(self):
        adsorbate_dict = self.poscar_generator.generate_adsorbates([1, 2])
        self.assertIsInstance(adsorbate_dict, dict)
        # More checks based on what you expect

if __name__ == "__main__":
    unittest.main()
