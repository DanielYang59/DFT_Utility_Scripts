#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Test objectives: Test the free energy calculations of
1. pH=0, external_potential=0:
    a. proton-electron pair (H+ + e-). Expect -3.3836 eV.
    b. hydroxide-electron pair (OH- + e-). Expect -10.0082 eV.

2. pH=0, external_potential=1:
    a. proton-electron pair (H+ + e-). Expect X eV.
    b. hydroxide-electron pair (OH- + e-). Expect X eV.

3. pH=7, external_potential=0:
    a. proton-electron pair (H+ + e-). Expect X eV.
    b. hydroxide-electron pair (OH- + e-). Expect X eV.

"""

import unittest
from src.computationalHydrogenElectrode import ComputationalHydrogenElectrode

class TestComputationalHydrogenElectrode(unittest.TestCase):
    def setUp(self):
        # Set up any common configuration or resources needed for the tests
        self.temperature = 298.15

    def test_calculate_proton_free_energy(self):
        che = ComputationalHydrogenElectrode(temperature=self.temperature, pH=0, external_potential=0)
        proton_free_energy = che.calculate_proton_free_energy()
        # Add assertions to verify the correctness of the result
        self.assertEqual(proton_free_energy, -3.3836)

    def test_calculate_hydroxide_free_energy(self):
        che = ComputationalHydrogenElectrode(temperature=self.temperature, pH=0, external_potential=0)
        hydroxide_free_energy = che.calculate_hydroxide_free_energy()
        # Add assertions to verify the correctness of the result
        self.assertEqual(hydroxide_free_energy, -10.0082)

if __name__ == "__main__":
    unittest.main()
