#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from pathlib import Path

from pymatgen.io.vasp import Vasprun

from .is_vasp_dir import is_vasp_dir


class VaspStatusChecker:
    def __init__(self, working_dir: Path) -> None:
        # Instead of raising an error, return None so that the workflow would not be interrupted
        if not working_dir.is_dir():
            self.job_type = None
            self.reason = "Directory not exists."

        elif not is_vasp_dir(working_dir):
            self.job_type = None
            self.reason = "Not a legal VASP directory."

        elif not (working_dir / "vasprun.xml").is_file():
            self.job_type = None
            self.reason = "vasprun.xml not found."

        # Import vasprun.xml file
        self.working_dir = working_dir
        self.vasprun = Vasprun(working_dir / "vasprun.xml")


    def check_job_type(self) -> str:
        # Pymatgen doesn't seem to have a proper method for this......yet.
        pass


    def check_convergence(self) -> bool:
        return self.vasprun.converged


    def get_energy(self) -> float:
        return self.vasprun.final_energy


def check_vasp_status():
    pass


if __name__ == "__main__":
    check_vasp_status()
