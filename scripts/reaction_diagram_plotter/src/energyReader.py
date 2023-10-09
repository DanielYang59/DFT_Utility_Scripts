#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pathlib import Path
import pandas as pd

class EnergyReader:
    def  __init__(self, intermediate_energy_file: Path, species_energy_file: Path,) -> None:
        """
        TODO:

        Args:
            intermediate_energy_file (Path): Path to the intermediate energy CSV file.
            species_energy_file (Path): Path to the species energy CSV file.
            external_potential (Union[float, int], optional): External potential in volts. Defaults to 0.


        """
        # Import intermediate energies and species energies
        self.intermediate_energies = self._import_energy_csv_file(intermediate_energy_file)
        self.species_energies = self._import_energy_csv_file(species_energy_file)

    def _import_energy_csv_file(self, file: Path, energy_name: str = "free_energy") -> Dict[str, float]:
        """
        Import and parse energy data from a CSV file into a dictionary.

        Args:
            file (Path): Path to the CSV file containing energy data.

        Raises:
            FileNotFoundError: If the CSV file is not found or has an illegal extension.

        Returns:
            Dict[str, float]: A dictionary where keys are column names and values are energy values.
        """
        # Check if the file exists and has a ".csv" extension
        if not file.is_file() or file.suffix != ".csv":
            raise FileNotFoundError(f"Energy CSV file '{file}' not found or illegal.")

        # Import energy CSV file using pandas and convert to dictionary
        energy_data = pd.read_csv(file)
        return dict(zip(energy_data['name'], energy_data[energy_name]))

    def _read_molecule_energy(self, name: str) -> float:
        pass

    def _read_ion_energy(self, name: str) -> float:
        pass

    def _read_intermediate_energy(self, name: str) -> float:
        pass

# Test area
if __name__ == "__main__":
    intermediate_energy_file=Path("../example_usage/example_intermediate_energies.csv"),
    species_energy_file=Path("../example_usage/example_species_energies.csv"),
