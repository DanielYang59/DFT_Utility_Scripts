#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# DEBUG: unreliable energy check
# TODO:

from pathlib import Path
from ase.io import read

from .is_vasp_dir import is_vasp_dir

class VaspDirChecker:
    """
    VaspDirChecker is a utility class designed to verify and analyze VASP
    (Vienna Ab initio Simulation Package) directories.

    The class provides the following functionalities:
        1. Checks if a given directory contains all essential VASP input files (INCAR, KPOINTS, POTCAR, POSCAR).
        2. Determines if a VASP job in the directory has successfully converged.
        3. Extracts the final energy of a converged VASP job from the OUTCAR file.
    """

    def __init__(self, dir_path: Path) -> None:
        """
        Initializes the VaspDirChecker object and checks if the directory
        contains all the essential VASP input files.

        Parameters:
            dir_path (Path): Path to the VASP directory to be checked.

        Raises:
            FileNotFoundError: If the directory is not a valid VASP directory.
        """
        # Check directory
        if not is_vasp_dir():
            raise FileNotFoundError("Essential VASP input files are missing.")

        # Import OUTCAR file
        self.outcar_path = self.dir_path / "OUTCAR"
        if not self.outcar_path.exists():
            raise FileNotFoundError("OUTCAR file not found.")

    def check_convergence(self) -> bool:
        """
        Checks if the VASP job in the directory has converged.

        Returns:
            bool: True if converged, False otherwise.
        """
        # Check if converged
        with self.outcar_path.open('r', encoding="utf-8") as f:
            for line in f:
                if "reached required accuracy" in line:
                    return True

        return False

    def get_final_energy(self) -> float:
        """
        Gets the final energy of the VASP job from the OUTCAR file using ASE.

        Returns:
            float: The final energy of the VASP job.

        Raises:
            FileNotFoundError: If the OUTCAR file is not found.
        """
        # Read
        atoms = read(self.outcar_path, format="vasp-out")
        return atoms.get_potential_energy()

def main() -> list:
    """
    Main function to be executed when this script is run directly.

    It first checks if the current working directory is a valid VASP directory.
    If it is, it prints the directory name, convergence status, and total energy.
    If not, it looks into all the subdirectories within the current directory
    and performs the same checks, printing a datasheet-style output with
    directory names, convergence statuses, and total energies as columns.
    """
    results = []
    current_dir = Path.cwd()

    print(f"{'Folder':<50} {'Converged':<15} {'Final Energy (eV)':<20}")

    try:
        vasp_checker = VaspDirChecker(current_dir)
        is_converged = vasp_checker.check_convergence()
        final_energy = vasp_checker.get_final_energy() if is_converged else "N/A"
        results.append([str(current_dir), is_converged, final_energy])

        print(f"{str(current_dir):<50} {str(is_converged):<15} {str(final_energy):<20}")
    except FileNotFoundError:
        print(f"{current_dir} is not a valid VASP directory. Checking subdirectories...")

        for subdir in current_dir.iterdir():
            if subdir.is_dir():
                try:
                    vasp_checker = VaspDirChecker(subdir)
                    is_converged = vasp_checker.check_convergence()
                    final_energy = vasp_checker.get_final_energy() if is_converged else "N/A"
                    results.append([str(subdir), is_converged, final_energy])

                    print(f"{str(subdir):<50} {str(is_converged):<15} {str(final_energy):<20}")
                except FileNotFoundError:
                    print(f"{str(subdir):<50} {'N/A':<15} {'N/A':<20}")
                    results.append([str(subdir), 'N/A', 'N/A'])

    return results

if __name__ == "__main__":
    main()
