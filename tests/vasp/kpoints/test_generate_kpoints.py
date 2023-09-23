#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
import warnings

from ....scripts.vasp.kpoints.generate_kpoints import generate_kpoints

class TestGenerateKpoints(unittest.TestCase):

    def test_valid_input(self):
        kpoints = [3, 3, 3]
        mesh_type = "g"
        expected_output = (
            "Regular k-point mesh          ! Type of k-point grid\n"
            "0                              ! 0 -> determine number of k points automatically\n"
            "Gamma-centered                     ! generate a Gamma-centered mesh\n"
            "3  3  3         ! subdivisions N_1, N_2 and N_3 along the reciprocal lattice vectors\n"
            "0  0  0                         ! optional shift of the mesh (s_1, s_2, s_3)\n"
        )
        self.assertEqual(generate_kpoints(kpoints, mesh_type), expected_output)

    def test_invalid_input_length(self):
        with self.assertRaises(ValueError):
            generate_kpoints([3, 3], "g")

    def test_invalid_input_type(self):
        with self.assertRaises(ValueError):
            generate_kpoints([3, -3, 3], "g")

    def test_high_value_warning(self):
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            generate_kpoints([3, 3, 101], "g")
            self.assertEqual(len(w), 1)
            self.assertTrue(issubclass(w[-1].category, UserWarning))

if __name__ == "__main__":
    unittest.main()
