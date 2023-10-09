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

    def __init__(self, intermediate_energy_file: Path, species_energy_file: Path, external_potential: Union[float, int] = 0, pH: Union[float, int] = 7, verbose: bool = True) -> None:
        """
        Initialize the class instance with energy files, external potential, and pH.

        Args:
            intermediate_energy_file (Path): Path to the intermediate energy CSV file.
            species_energy_file (Path): Path to the species energy CSV file.
            external_potential (Union[float, int], optional): External potential in volts. Defaults to 0.
            pH (Union[float, int], optional): pH value (0 to 14). Defaults to 7.
            verbose (bool, optional): global verbose level. Defaults to True.

        Raises:
            TypeError: If external_potential or pH is not a float or an integer.
            ValueError: If pH is not within the range of 0 to 14.
            TypeError: If verbose is not boolean.
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

        # Check and set verbose level
        if not isinstance(verbose, bool):
            raise TypeError("Illegal data type for verbose.")
        self.verbose = verbose

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
            if not isinstance(num, int) or num <= 0:
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
                raise ValueError(f"Unrecognizable species type for '{name}'.")

        return energy

    def _calculate_energy_change_for_step(self, pathway: dict) -> tuple:
        """
        Calculate the energy change for a given reaction step based on the provided pathway details.

        Args:
            pathway (dict): A dictionary containing 'reactants' and 'products' keys, each with their respective components.

        Returns:
            tuple: A tuple containing the total energies of (products, reactants).

        Calculates the energy change for the given reaction step by computing the energies of products and reactants separately.
        The input 'pathway' dictionary should have 'reactants' and 'products' keys, where each key maps to a dictionary of
        molecular components and their respective quantities.

        Example:
            For pathway input:
            {
                "reactants": {"A": 2, "B": 1},
                "products": {"C": 1, "D": 1}
            }

            The returned tuple would be (energy_of_products, energy_of_reactants).

        """
        # Calculate energy for products
        products_energy = self._calculate_half_reaction_energy(pathway["products"])

        # Calculate energy for reactants
        reactants_energy = self._calculate_half_reaction_energy(pathway["reactants"])

        return products_energy, reactants_energy

    def calculate_energy_change(self, reaction_pathways: Dict[int, dict]) -> Dict[int, float]:
        """
        Calculate the energy change for each reaction step in the provided reaction pathways.

        Args:
            reaction_pathways (dict): A dictionary containing reaction steps as keys and their respective pathway details.

        Returns:
            Dict[int, float]: A dictionary where keys represent reaction steps, and values represent energy changes.

        Raises:
            ValueError: If the input data type is not a dictionary or if the dictionary is empty.
        """
        # Check and take reaction pathways dict
        if not isinstance(reaction_pathways, dict) or not dict:
            raise ValueError("Illegal data type or empty reaction pathway found.")
        self.reaction_pathways = reaction_pathways

        # Calculate energy change for each reaction step
        energy_changes = {}
        for index, pathway in self.reaction_pathways.items():
            # Calculate products and reactants energies
            products_energy, reactants_energy = self._calculate_energy_change_for_step(pathway)

            # Calculate energy change
            energy_change = products_energy - reactants_energy
            energy_changes[index] = energy_change

            # Verbose
            if self.verbose:
                print(f"Step {index + 1}: product_energy {products_energy} eV, reactant_energy {reactants_energy} eV, energy_change {energy_change}")

        return energy_changes

# Test area
if __name__ == "__main__":
    # Import reaction pathway
    pathway = {1: {'reactants': {'*': 1, 'CO2': 1, 'H+': 1, 'e-': 1}, 'products': {'*COOH': 1}}, 2: {'reactants': {'*COOH': 1, 'H+': 1, 'e-': 1}, 'products': {'*CO': 1, 'H2O_l': 1}}, 3: {'reactants': {'*CO': 1, 'H2O_l': 1, 'H+': 1, 'e-': 1}, 'products': {'*CHO': 1, 'H2O_l': 1}}, 4: {'reactants': {'*CHO': 1, 'H2O_l': 1, 'H+': 1, 'e-': 1}, 'products': {'*CH2O': 1, 'H2O_l': 1}}, 5: {'reactants': {'*CH2O': 1, 'H2O_l': 1, 'H+': 1, 'e-': 1}, 'products': {'*OCH3': 1, 'H2O_l': 1}}, 6: {'reactants': {'*OCH3': 1, 'H2O_l': 1, 'H+': 1, 'e-': 1}, 'products': {'*O': 1, 'H2O_l': 1, 'CH4_g': 1}}, 7: {'reactants': {'*O': 1, 'H2O_l': 1, 'CH4_g': 1, 'H+': 1, 'e-': 1}, 'products': {'*OH': 1, 'H2O_l': 1, 'CH4_g': 1}}, 8: {'reactants': {'*OH': 1, 'H2O_l': 1, 'CH4_g': 1, 'H+': 1, 'e-': 1}, 'products': {'*': 1, 'H2O_l': 2, 'CH4_g': 1}}}

    # Initiate reaction energy calculator
    calculator = ReactionEnergyCalculator(
        intermediate_energy_file=Path("../example_usage/example_intermediate_energies.csv"),
        species_energy_file=Path("../example_usage/example_species_energies.csv"),
        external_potential=0
        )

    # Calculate energy change
    calculator.calculate_energy_change(pathway)
