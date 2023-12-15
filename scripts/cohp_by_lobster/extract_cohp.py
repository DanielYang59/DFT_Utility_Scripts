#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# https://pymatgen.org/pymatgen.io.lobster.html
# https://pymatgen.org/pymatgen.electronic_structure.html

# Tutorial: https://matgenb.materialsvirtuallab.org/2019/01/11/How-to-plot-and-evaluate-output-files-from-Lobster.html

import itertools
from enum import Enum
import numpy as np
from pathlib import Path
from typing import List, Tuple
from pymatgen.electronic_structure.cohp import CompleteCohp
from pymatgen.electronic_structure.plotter import CohpPlotter

# NOTE: WARNING: labels in "COHP.lobtser" and "ICOHP.lobster" might be different, according to: https://matgenb.materialsvirtuallab.org/2019/01/11/How-to-plot-and-evaluate-output-files-from-Lobster.html


class cohpExtractor:
    def __init__(self, cohp_dir: Path) -> None:
        # Check core files
        if not (cohp_dir / 'COHPCAR.lobster').is_file():
            raise FileNotFoundError(f"COHPCAR.lobster not found in {cohp_dir}.")
        if not (cohp_dir / 'POSCAR').is_file():
            raise FileNotFoundError(f"POSCAR not found in {cohp_dir}.")

        # Load COHP data from file
        self.complete_cohp = CompleteCohp.from_file(fmt='LOBSTER', filename=cohp_dir / 'COHPCAR.lobster', structure_file= cohp_dir / 'POSCAR')


    def _get_atom_pairs(self) -> List[str]:
        # TODO: return label list
        """
        Prompt the user to choose an atom pair by label.

        Atom pairs are labeled starting from 1. User input is validated to be within the valid range.

        Returns:
            str: The chosen atom pair label (1-indexed).

        Notes:
            This is defined as "label": https://pymatgen.org/pymatgen.electronic_structure.html.
        """
        # Let the user choose an atom pair by label
        num_atom_pairs = len(self.complete_cohp.bonds)
        label_prompt = f"{num_atom_pairs} atom pairs found. Please specify the pair label (1-indexed): "

        while True:
            try:
                label = int(input(label_prompt))
                # Check if the label is within the valid range
                assert 1 <= label <= num_atom_pairs
                break  # Break out of the loop if the input is valid

            except ValueError:
                print("Invalid input. Please enter a valid integer.")

            except AssertionError:
                print(f"Invalid label. Please enter a label between 1 and {num_atom_pairs}.")

        return label


    def _get_orbitals(self) -> List[str]:
        # TODO: return orbital list
        """
        Prompt the user to choose an orbital pair.

        Orbital pairs are represented as keys in a dictionary. User input is validated to be within the valid keys.

        Returns:
            str: The chosen orbital pair key.
        """
        # Let the user choose an orbital pair
        orbital_pairs = self.complete_cohp.orbitals
        # DEBUG
        num_orbital_pairs = len(orbital_pairs)

        # Display available keys for user selection
        print("Available orbital pair keys:")
        for key, entry in orbital_pairs.items():
            print(f"{key}: {entry}")  # DEBUG

        while True:
            try:
                orbital = input("Please specify the orbital pair key: ")
                # Check if the key is within the valid keys
                assert orbital in orbital_pairs
                break  # Break out of the loop if the input is valid

            except AssertionError:
                print("Invalid key. Please choose a valid orbital pair key.")

        return orbital


    def _extract_and_sum_cohp(self, labels: List[str], orbitals: List[str]) -> Tuple[np.ndarray, np.ndarray]:
        class Spin(Enum):
            up = 1
            down = -1

        spin_up_total = 0  # DEBUG: would this work?
        spin_down_total = 0

        for lab in labels:
            for orb in orbitals:
                spin_up_cohp = self.complete_cohp.orb_res_cohp[lab][orb]["COHP"][Spin.up]
                spin_down_cohp = self.complete_cohp.orb_res_cohp[lab][orb]["COHP"][Spin.down]

                spin_up_total += spin_up_cohp
                spin_down_total += spin_down_cohp

        return spin_up_total, spin_down_total


    def extract_cohp(self) -> Tuple[np.ndarray, np.ndarray]:
        # TODO: add docstring
        # Get atom pair and orbital pair from user
        atom_pairs = self._get_atom_pairs()
        orbital_paris = self._get_orbitals()

        # Calculate summed COHP accordingly
        summed_cohp = self._extract_and_sum_cohp(atom_pairs, orbital_paris)  # DEBUG

        print(summed_cohp)

        return summed_cohp


    def save_to_file(self, savename: Path = Path.cwd()/"cohp.dat") -> None:
        pass


    def show_plot(self):
        pass


def extract_cohp(show_plot: bool = False):
    # Initialize COHP extractor
    test_dir = Path.cwd()   # DEBUG
    extractor = cohpExtractor(test_dir)

    extractor.extract_cohp()


if __name__ == "__main__":
    extract_cohp()
