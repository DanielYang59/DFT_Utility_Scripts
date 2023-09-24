#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
from pathlib import Path

from ....scripts.vasp.potcar.generate_potcar import PotcarGenerator

class TestPotcarGenerator(unittest.TestCase):

    def setUp(self):
        self.potcar_gen = PotcarGenerator()
        self.test_data_path = Path(__file__).parent / "test_data"

    def test_valid_MgO(self):
        elements = self.potcar_gen.get_elements_from_poscar(self.test_data_path / "POSCAR_valid_MgO")
        self.assertEqual(elements, ["Mg", "O"])

    def test_valid_Si(self):
        elements = self.potcar_gen.get_elements_from_poscar(self.test_data_path / "POSCAR_valid_Si")
        self.assertEqual(elements, ["Si"])

    def test_warning_many_elements(self):
        elements = self.potcar_gen.get_elements_from_poscar(self.test_data_path / "POSCAR_warning_many_element")
        with self.assertWarns(UserWarning):
            self.potcar_gen.generate_potcar(elements)

    def test_invalid_empty_element(self):
        with self.assertRaises(RuntimeError):
            elements = self.potcar_gen.get_elements_from_poscar(self.test_data_path / "POSCAR_invalid_empty_element")

if __name__ == "__main__":
    unittest.main()
