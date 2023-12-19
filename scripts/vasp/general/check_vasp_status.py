#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# TODO: default INCAR tags are not handled


from pathlib import Path

from pymatgen.io.vasp import Vasprun, Incar

from .is_vasp_dir import is_vasp_dir


class VaspStatusChecker:
    # TODO:

    def __init__(self, working_dir: Path) -> None:
        """
        Initialize the VaspStatusChecker.

        Args:
            working_dir (Path): The path to the VASP calculation directory.
        """
        # Instead of raising an error, return None so that the workflow would not be interrupted
        if not working_dir.is_dir():
            self.job_type = None
            self.comment = "Directory not exists."

        elif not is_vasp_dir(working_dir):
            self.job_type = None
            self.comment = "Not a legal VASP directory."

        elif not (working_dir / "vasprun.xml").is_file():
            self.job_type = None
            self.comment = "vasprun.xml not found."

        # Import vasprun.xml file
        self.working_dir = working_dir
        self.vasprun = Vasprun(working_dir / "vasprun.xml")
        self.incar = Incar().from_file(working_dir / "INCAR")


    def check_job_type(self) -> str:
        """
        Check and return the type of the VASP calculation job.

        Returns:
            str: The type of the VASP calculation job.

        Notes:
            Pymatgen doesn't seem to have a proper method for this... yet.

        The job types are determined based on specific INCAR parameters. The recognized job types
        include 'cell_opt' for cell optimization, 'ion_opt' for ionic optimization, 'scf' for
        self-consistent field calculations, and 'unknown' for jobs with an unknown type.

        - Job type 'cell_opt':
          Conditions: ISIF = 3; IBRION = 2; NSW > 0
          Reference: https://www.vasp.at/tutorials/latest/bulk/part2/#bulk-e05

        - Job type 'ion_opt':
          Conditions: ISIF = 2; IBRION = 2; NSW > 0
          Reference: https://www.vasp.at/tutorials/latest/molecules/part3/

        - Job type 'scf':
          Conditions: IBRION = -1 or NSW = 0

        - Job type 'unknown':
          Conditions: None of the above conditions are met.
        """
        # Job type: Cell optimization
        # ISIF = 3; IBRION = 2; NSW > 0
        # Reference: https://www.vasp.at/tutorials/latest/bulk/part2/#bulk-e05
        if self.incar["ISIF"] == 3 and self.incar["IBRION"] == 2 and self.incar["NSW"] > 0:
            self.job_type = "cell_opt"
            self.comment = "cell optimization"


        # Job type: Ionic optimization
        # ISIF = 2; IBRION = 2; NSW > 0
        # Reference: https://www.vasp.at/tutorials/latest/molecules/part3/
        elif self.incar["ISIF"] == 2 and self.incar["IBRION"] == 2 and self.incar["NSW"] > 0:
            self.job_type = "ion_opt"
            self.comment = "Ion optimization"


        # Job type: SCF
        # IBRION = -1; NSW = 0
        elif self.incar["IBRION"] == -1 or self.incar["NSW"] == 0:
            self.job_type = "scf"
            self.comment = "self-consistent field"


        # Job type: Unknown
        else:
            self.job_type = "unknown"
            self.comment = "Unknown job type"


    def check_convergence(self) -> bool:
        """
        Check and return the convergence status (both ionic and electronic) of the VASP calculation.

        Returns:
            bool: True if the calculation has converged, False otherwise.
        """
        return self.vasprun.converged


    def get_energy(self) -> float:
        """
        Return the final energy of the VASP calculation.

        Returns:
            float: The final energy of the VASP calculation.
        """
        return self.vasprun.final_energy


def check_vasp_status():
    pass


if __name__ == "__main__":
    check_vasp_status()
