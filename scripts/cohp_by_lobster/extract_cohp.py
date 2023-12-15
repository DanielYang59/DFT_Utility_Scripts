#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# https://pymatgen.org/pymatgen.io.lobster.html
# https://pymatgen.org/pymatgen.electronic_structure.html

# Tutorial: https://matgenb.materialsvirtuallab.org/2019/01/11/How-to-plot-and-evaluate-output-files-from-Lobster.html

from pathlib import Path
from pymatgen.electronic_structure.cohp import CompleteCohp
from pymatgen.electronic_structure.plotter import CohpPlotter

# NOTE: energy from cohp should already by referenced to fermi level

# WARNING: labels in "COHP.lobtser" and "ICOHP.lobster" might be different according to: https://matgenb.materialsvirtuallab.org/2019/01/11/How-to-plot-and-evaluate-output-files-from-Lobster.html


class cohpExtractor:
    def __init__(self, cohp_dir: Path) -> None:
        # Load COHP data
        self._load_cohp_data(working_dir = cohp_dir)


    def _load_cohp_data(self, working_dir: Path) -> None:
        """
        Load COHP (Crystal Orbital Hamilton Population) data from a Lobster calculation.

        This method reads COHPCAR.lobster and POSCAR files from the specified directory
        and initializes the `complete_cohp` attribute with the loaded data.

        Parameters:
            working_dir (Path): The path to the directory containing COHPCAR.lobster and POSCAR files.

        Raises:
            FileNotFoundError: If either COHPCAR.lobster or POSCAR is not found in the specified directory.

        Notes:
            Reference: https://pymatgen.org/pymatgen.electronic_structure.html

        Returns:
            None
        """
        # Check core files
        if not (working_dir / 'COHPCAR.lobster').is_file():
            raise FileNotFoundError(f"COHPCAR.lobster not found in {working_dir}.")
        if not (working_dir / 'POSCAR').is_file():
            raise FileNotFoundError(f"POSCAR not found in {working_dir}.")

        # Load complete COHP
        self.complete_cohp = CompleteCohp.from_file(fmt='LOBSTER', filename=working_dir / 'COHPCAR.lobster', structure_file= working_dir / 'POSCAR')


    def get_atom_pair(self) -> str:
        """
        Prompt the user to choose an atom pair by label.

        Atom pairs are labeled starting from 1. User input is validated to be within the valid range.

        Returns:
            str: The chosen atom pair label (1-indexed).
        """
        # This is defined as "label": https://pymatgen.org/pymatgen.electronic_structure.html
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

        return str(label)


    def get_orbital(self) -> str:
        pass


    def save_to_file(self, savename: Path = Path.cwd()/"cohp.dat") -> None:
        pass


    def show_plot(self):
        pass


def extract_cohp(show_plot: bool = False):
    # Initialize COHP extractor
    extractor = cohpExtractor(Path.cwd())

    # DEBUG info:
    print()


if __name__ == "__main__":
    extract_cohp()
