#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pathlib import Path
from typing import Union, Dict
import pandas as pd
import warnings

class ReactionEnergyCalculator:
    """
    TODO:
    """

    def __init__(self, intermediate_energy_file: Path, species_energy_file: Path, external_potential: Union[float, int] = 0, pH: Union[float, int] = 7) -> None:
        """
        Initialize the class instance with energy files, external potential, and pH.

        Args:
            intermediate_energy_file (Path): Path to the intermediate energy CSV file.
            species_energy_file (Path): Path to the species energy CSV file.
            external_potential (Union[float, int], optional): External potential in volts. Defaults to 0.
            pH (Union[float, int], optional): pH value (0 to 14). Defaults to 7.

        Raises:
            TypeError: If external_potential or pH is not a float or an integer.
            ValueError: If pH is not within the range of 0 to 14.
        """
        # Import intermediate energies and species energies
        self.intermediate_energies = self._import_energy_csv_file(intermediate_energy_file)
        self.species_energies = self._import_energy_csv_file(species_energy_file)

        # Check and set external_potential
        if not isinstance(external_potential, (float, int)):
            raise TypeError("External potential must be a float or an integer.")
        self.external_potential = external_potential

        # Check and set pH
        if not isinstance(pH, (float, int)):
            raise TypeError("pH must be a float or an integer.")
        if not 0 <= pH <= 14:
            raise ValueError("pH must be within the range of 0 to 14.")
        self.pH = pH

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

    def _calculate_half_reaction_energy(self, species: Dict[str, int]) -> float:
        """TODO:

        Args:
            species (Dict[str, int]): _description_

        Returns:
            float: _description_
        """
        # Calculate half reaction energy
        energy = 0

        # Check half reaction dict
        for name, num in species.items():
            # Validate species name and number
            if not isinstance(name, str):
                raise TypeError(f"Name for species {name} is not in expected type str, got {type(name)}.")
            if not isinstance(num, int) or num <= 1:
                raise ValueError(f"Get illegal stoichiometric number '{num}' for species {name}.")

            # Calculate species energy based on its type
            # Species is "ion"
            if name.endswith("-") or name.endswith("+"):
                pass

            # Species is "reaction intermediate"
            elif name.startswith("*"):
                pass

            # Species is "molecule"
            elif name.endswith("_g") or name.endswith("_l"):
                pass

            # Unrecognizable species type
            else:
                raise ValueError(f"Unrecognizable species type for {name}.")

        return energy

    def _calculate_energy_change_for_step(self, pathway: dict, warn_threshold: float = 50) -> float:
        """Calculate energy change for given reaction step.

        Args:
            pathway (dict): _description_

        Returns:
            float: _description_

        """
        # Calculate energy for products
        products_energy = self._calculate_half_reaction_energy(pathway["products"])
        print(products_energy)

        import sys
        sys.exit()
        #DEBUG
        # Calculate energy for reactants
        reactants_energy = self._calculate_half_reaction_energy(pathway["reactants"])

        # Calculate energy change
        energy_change = products_energy - reactants_energy

        # Warn if suspicious energy change value
        if energy_change >= warn_threshold or energy_change <= -warn_threshold:
            warnings.warn(f"Large free energy change of {energy_change} eV found.")

        return energy_change

    def calculate_energy_change(self) -> Dict[int, float]:
        """Calculate energy change for each reaction step.

        Returns:
            Dict[int, float]: _description_
        """
        # Calculate energy change for each reaction step
        energy_change = {}
        for index, pathway in self.reaction_pathway.items():
            energy_change[index] = self._calculate_energy_change_for_step(pathway)

        return energy_change

# Test area
if __name__ == "__main__":
    pass
