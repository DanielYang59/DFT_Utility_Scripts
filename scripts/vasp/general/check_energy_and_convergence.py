#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pathlib import Path
from pymatgen.io.vasp.outputs import Outcar

class VaspDirChecker:
    """
    VaspDirChecker is a utility class designed to verify and analyze VASP
    (Vienna Ab initio Simulation Package) directories.

    The class provides the following functionalities:
        1. Checks if a given directory contains all essential VASP input files (INCAR, KPOINTS, POTCAR, POSCAR).
        2. Determines if a VASP job in the directory has successfully converged.
        3. Extracts the final energy of a converged VASP job from the OUTCAR file.
    """

    def __init__(self, dir_path: Path):
        """
        Initializes the VaspDirChecker object and checks if the directory
        contains all the essential VASP input files.

        Parameters:
            dir_path (Path): Path to the VASP directory to be checked.

        Raises:
            FileNotFoundError: If the directory is not a valid VASP directory.
        """
        self.dir_path = dir_path
        if not self._check_input_files():
            raise FileNotFoundError("Essential VASP input files are missing.")

    def _check_input_files(self) -> bool:
        """
        Checks if all four essential VASP input files exist in the directory.

        Returns:
            bool: True if all files exist, False otherwise.
        """
        required_files = ["INCAR", "KPOINTS", "POTCAR", "POSCAR"]
        for file in required_files:
            if not (self.dir_path / file).exists():
                return False
        return True

    def check_convergence(self) -> bool:
        """
        Checks if the VASP job in the directory has converged.

        Returns:
            bool: True if converged, False otherwise.
        """
        outcar_path = self.dir_path / "OUTCAR"
        if not outcar_path.exists():
            return False  # OUTCAR not found

        outcar = Outcar(str(outcar_path))
        return outcar.converged

    def get_final_energy(self) -> float:
        """
        Gets the final energy of the VASP job from the OUTCAR file.

        Returns:
            float: The final energy of the VASP job.

        Raises:
            FileNotFoundError: If the OUTCAR file is not found.
        """
        outcar_path = self.dir_path / "OUTCAR"
        if not outcar_path.exists():
            raise FileNotFoundError("OUTCAR file not found.")

        outcar = Outcar(str(outcar_path))
        return outcar.final_energy
