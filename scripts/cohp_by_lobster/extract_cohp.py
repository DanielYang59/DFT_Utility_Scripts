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
    def __init__(self, cohp_dir: Path = Path.cwd()) -> None:
        # Load COHP data
        self._load_cohp_data(working_dir=cohp_dir)


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


    def get_interation_pair(self) -> None:  # NOTE: double check method name and return hint
        # This seems to be defined as "label" in the "get_cohp_by_label" method
        # by pymatgen: https://pymatgen.org/pymatgen.electronic_structure.html
        pass


    def save_to_file(self, savename: Path = Path.cwd()/"cohp.dat") -> None:
        pass


    def show_plot(self):
        pass


def extract_cohp(show_plot: bool = False):
    pass


if __name__ == "__main__":
    extract_cohp()
