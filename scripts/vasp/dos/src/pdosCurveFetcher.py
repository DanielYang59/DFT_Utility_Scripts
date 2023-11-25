#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
from typing import List, Tuple
from .vasprunXmlReader import VasprunXmlReader

class PdosCurveFetcher:
    def __init__(self, vasprunreader: VasprunXmlReader) -> None:
        assert isinstance(vasprunreader, VasprunXmlReader)
        self.vasprunreader = vasprunreader

    def _fetch_and_cat_atoms(self, atom_indexes: List[int], spin_index: int) -> np.ndarray:
        """
        Fetches and concatenates the pDOS for specified atoms and spin index.

        Parameters:
            atom_indexes (List[int]): A list of atom indices for which to fetch pDOS.
            spin_index (int): The spin index, either 1 or 2.

        Returns:
            np.ndarray: A 3D NumPy array representing the concatenated pDOS for the specified atoms.
            The shape of the array is (number_of_atoms, NEDOS, numOrbitals).

        Raises:
            AssertionError: If the spin_index is not 1 or 2.
        """
        # Check spin index
        assert spin_index in {1, 2}

        # Fetch and concatenate pDOS for each atom
        return np.stack([self.vasprunreader.read_energy_and_pdos(index, spin_index) for index in atom_indexes], axis=0)

    def _select_pdos_by_orbital(self, pdos_array: np.ndarray, orbital_selections: List[int]) -> Tuple[np.ndarray, np.ndarray]:
        """
        Selects pDOS by orbital based on the provided orbital selections.

        Parameters:
            pdos_array (np.ndarray): Input array of shape (X, Y, 9) representing pDOS for each atom and orbital.
            orbital_selections (List[int]): List of orbital selections to include in the final result.

        Returns:
            np.ndarray: Array representing the selected pDOS based on the orbital selections.
          The shape of the array is (Y,) if the original pDOS array has shape (X, Y, 9).
          The array is obtained by summing the pDOS along the first axis and then
          dot-multiplying the result with the orbital selections.

        Notes:
        - If the shape of the stacked pDOS array is (X, 9), the dot-multiplication is performed
          with the first 9 elements of the orbital selections.
        - If the shape is (X, 16), the dot-multiplication is performed with all elements of
          the orbital selections.

        """
        # Separate energy and pDOS array
        energy_array = pdos_array[:, :, 0]
        pdos_array = pdos_array[:, :, 1: ]

        # Compress energy array
        energy_array = np.squeeze(energy_array[0, :])

        # Select pDOS by orbital
        stacked_pdos_array = np.sum(pdos_array, axis=0)

        if stacked_pdos_array.shape[1] == 9:
            return energy_array, np.dot(stacked_pdos_array, np.array(orbital_selections[:9]))
        else:
            return energy_array, np.dot(stacked_pdos_array, np.array(orbital_selections))

    def fetch_curve(self, curve_info: list, ispin: int) -> Tuple[np.ndarray, np.ndarray]:
        """
        Fetches and processes partial density of states (pDOS) data based on the provided curve information.

        Parameters:
        - curve_info (List): List containing curve information, where the first element is a list
          of atom indexes, and the remaining elements are orbital selections.
        - ispin (int): Integer representing the spin index, either 1 or 2.

        Returns:
        - Tuple[np.ndarray, np.ndarray]: A tuple containing two arrays representing the selected pDOS:
          1. Array for spin-up pDOS with orbital selections.
          2. Array for spin-down pDOS with orbital selections (or np.nan if ispin is 1).

        Raises:
        - AssertionError: If the length of orbital selections is not 9 or 16, or if ispin is not 1 or 2.

        Notes:
        - The `curve_info` parameter should contain atom indexes as the first element and
          orbital selections as the remaining elements.
        - The `ispin` parameter represents the spin index, where 1 is for spin-up and 2 is for spin-down.
        - The resulting arrays represent the selected pDOS with orbital selections.

        """
        # Separate atom indexes and orbital selections
        atom_indexes = curve_info[0]
        orbital_selections = curve_info[1:]
        assert len(orbital_selections) in {9, 16}
        assert ispin in {1, 2}

        # Fetch pDOS data and include orbital selections
        spin_up_pdos = self._fetch_and_cat_atoms(atom_indexes, spin_index=1)
        energy_array, spin_up_pdos_orbital_selected = self._select_pdos_by_orbital(spin_up_pdos, orbital_selections)

        if ispin == 2:
            spin_down_pdos = self._fetch_and_cat_atoms(atom_indexes, spin_index=2)
            energy_array, spin_down_pdos_orbital_selected = self._select_pdos_by_orbital(spin_down_pdos, orbital_selections)

        else:
            spin_down_pdos = None

        assert energy_array.shape == spin_up_pdos_orbital_selected.shape
        return energy_array, spin_up_pdos_orbital_selected, spin_down_pdos_orbital_selected
