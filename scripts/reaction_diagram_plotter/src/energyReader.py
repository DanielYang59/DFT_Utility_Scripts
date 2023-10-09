#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pathlib import Path
import pandas as pd
from typing import Dict

class EnergyReader:
    """
    A utility class for reading energy data from CSV files and providing energy values for species and intermediates.

    Methods:
        __init__(intermediate_energy_file: Path, species_energy_file: Path, energy_type: str = "free_energy") -> None:
            Initialize an instance of the energy reader with input files and energy type.

        read_molecule_or_ion_energy(name: str) -> float:
            Retrieve energy value for a molecule or ion based on its name.

        read_intermediate_energy(name: str) -> float:
            Retrieve energy value for an intermediate species based on its name.

    Args:
        intermediate_energy_file (Path): Path to the intermediate energy CSV file.
        species_energy_file (Path): Path to the species energy CSV file.
        energy_type (str, optional): Type of energy to extract from the CSV files. Defaults to "free_energy".

    Raises:
        TypeError: If 'energy_type' is not a string.
        FileNotFoundError: If the CSV file is not found or has an illegal extension.
        ValueError: If extracted energy data is empty or illegal.

    The `EnergyReader` class provides methods to read energy data from CSV files. It initializes by importing
    intermediate and species energies from the specified CSV files. Energy values can be retrieved for molecules,
    ions, and intermediates based on their names.


    """
    def  __init__(self, intermediate_energy_file: Path, species_energy_file: Path, energy_type: str = "free_energy") -> None:
        """
        Initialize an instance of the energy calculator with given input files and energy type.

        Args:
            intermediate_energy_file (Path): Path to the intermediate energy CSV file.
            species_energy_file (Path): Path to the species energy CSV file.
            energy_type (str, optional): Type of energy to extract from the CSV files.
                Defaults to "free_energy".

        Raises:
            TypeError: If 'energy_type' is not a string.

        Initializes the energy calculator by importing intermediate energies and species energies
        from the specified CSV files. The 'energy_type' parameter determines which type of energy
        is extracted from the CSV files. It defaults to "free_energy". Accepted energy types should
        match the column names in the CSV files.

        """
        # Validate energy type
        if not isinstance(energy_type, str):
            raise TypeError("Illegal datatype for 'energy_type'.")
        self.energy_type = energy_type

        # Import intermediate energies and species energies
        self.intermediate_energies = self._import_energy_csv_file(intermediate_energy_file)
        self.species_energies = self._import_energy_csv_file(species_energy_file)

    def _import_energy_csv_file(self, file: Path) -> Dict[str, float]:
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
        energy_dict = dict(zip(energy_data['name'], energy_data[self.energy_type]))

        if not energy_dict:
            raise ValueError(f"Empty energy dict extracted from {file}.")
        return energy_dict

    def read_molecule_or_ion_energy(self, name: str) -> float:
        """
        Retrieve energy value for a molecule or ion based on its name.

        Args:
            name (str): The name of the molecule or ion.

        Returns:
            float: The energy value for the specified molecule or ion.

        Raises:
            ValueError: If the energy value is not a valid float or if it is empty.
        """
        energy = self.species_energies[name]

        if not isinstance(energy, float) or not energy:
            raise ValueError(f"Illegal energy {energy} found for {name}.")

        return energy

    def read_intermediate_energy(self, name: str) -> float:
        """
        Retrieve energy value for an intermediate species based on its name.

        Args:
            name (str): The name of the intermediate species.

        Returns:
            float: The energy value for the specified intermediate species.

        Raises:
            ValueError: If the energy value is not a valid float or if it is empty.
        """
        energy = self.intermediate_energies[name]

        if not isinstance(energy, float) or not energy:
            raise ValueError(f"Illegal energy {energy} found for {name}.")

        return energy
