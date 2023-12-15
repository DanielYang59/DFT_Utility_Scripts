#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# Check Pymatgen: https://pymatgen.org/pymatgen.io.lobster.html
# reference: https://gist.github.com/lan496/ee0bd7a52df99029ac0aacbe69f2bf57

from pathlib import Path
from pymatgen.electronic_structure.cohp import CompleteCohp
from pymatgen.electronic_structure.plotter import CohpPlotter

# NOTE: energy from cohp should already by referenced to fermi level


class cohpExtractor:
    def __init__(self) -> None:
        pass


    def load_cohp_data(self) -> None:
        pass


    def get_interation_pair(self) -> None:  # NOTE: double check method name and return hint
        pass


    def save_to_file(self, savename: Path = Path.cwd()/"cohp.dat") -> None:
        pass


    def show_plot(self):
        pass


def extract_cohp(show_plot: bool = False):
    pass


if __name__ == "__main__":
    extract_cohp()
