#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import Union, Dict

from .energyReader import EnergyReader
from .reactionStep import ReactionStep
from .computationalHydrogenElectrode import ComputationalHydrogenElectrode

class ReactionEnergyCalculator:
    """
    A class for calculating energy changes in chemical reaction pathways.

    Methods:
        __init__(external_potential: Union[float, int] = 0, pH: Union[float, int] = 7, verbose: bool = True) -> None:
            Initialize the class instance with external potential and pH.

        _calculate_half_reaction_energy(species: Dict[str, int]) -> float:
            Calculate the half reaction energy based on the given species and their stoichiometric numbers.

        _calculate_energy_change_for_step(pathway: dict) -> tuple:
            Calculate the energy change for a given reaction step based on the provided pathway details.

        calculate_energy_change(reaction_pathways: Dict[int, dict], energy_reader: EnergyReader) -> Dict[int, float]:
            Calculate the energy change for each reaction step in the provided reaction pathways.

    Args:
        external_potential (Union[float, int], optional): External potential in volts. Defaults to 0.
        pH (Union[float, int], optional): pH value (0 to 14). Defaults to 7.
        verbose (bool, optional): Global verbose level. Defaults to True.

    Raises:
        TypeError: If external_potential or pH is not a float or an integer.
        ValueError: If pH is not within the range of 0 to 14.
        TypeError: If verbose is not boolean.
        ValueError: If the input data type for reaction pathways or energy reader is incorrect.

    The `ReactionEnergyCalculator` class provides methods to calculate energy changes for chemical reaction pathways.
    The `calculate_energy_change` method accepts a dictionary of reaction pathways and an `EnergyReader` instance
    to calculate the energy change for each reaction step. The class uses the provided external potential and pH
    values in the energy calculations. Verbose output can be controlled using the `verbose` parameter.
    """

    def __init__(self, external_potential: Union[float, int] = 0, pH: Union[float, int] = 0, temperature: Union[float, int] = 298.15, verbose: bool = True) -> None:
        """
        Initialize the class instance with external potential and pH.

        Args:
            external_potential (Union[float, int], optional): External potential in volts. Defaults to 0.
            pH (Union[float, int], optional): pH value (0 to 14). Defaults to 0.
            temperature (Union[float, int], optional): temperature in K. Defaults to 298.15.
            verbose (bool, optional): global verbose level. Defaults to True.

        Raises:
            TypeError: If external_potential or pH is not a float or an integer.
            ValueError: If pH is not within the range of 0 to 14.
            TypeError: If verbose is not boolean.
        """
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

        # Check and set temperature
        if not isinstance(temperature, (float, int)):
            raise TypeError("Temperature must be a float or an integer.")
        if temperature < 0:
            raise ValueError("Temperature in K cannot be smaller than 0.")
        self.temperature = temperature

        # Check and set verbose level
        if not isinstance(verbose, bool):
            raise TypeError("Illegal data type for verbose.")
        self.verbose = verbose

    def _fetch_species_energies(self, species_dict: Dict[str, Union[float, int]]) -> Dict[str, float]:
        pass

    def calculate_energy_changes(self, reaction_pathways: Dict[int, dict], energy_reader: EnergyReader) -> Dict[int, float]:
        """
        Calculate the energy changes for each reaction step in the provided reaction pathways.

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

        # Check and take energy reader
        if not isinstance(energy_reader, EnergyReader):
            raise ValueError("Illegal data type for energy reader.")
        self.energy_reader = energy_reader

        # Calculate energy change for each reaction step
        energy_changes = {}
        for index, pathway in self.reaction_pathways.items():
            # Initiate each reaction step
            reaction_step = ReactionStep(self.temperature, self.pH, self.external_potential)

            # Set species and energies
            reaction_step.set_reactants(pathway["reactants"], self._fetch_species_energies(pathway["reactants"]))
            reaction_step.set_products(pathway["products"], self._fetch_species_energies(["products"]))

            # Add corrections
            pH_correction = reaction_step.calculate_pH_correction()
            external_potential_correction = reaction_step.calculate_external_potential_correction()

            # Calculate free energy change with corrections
            energy_changes[index] = reaction_step.calculate_free_energy_change() + pH_correction + external_potential_correction

        return energy_changes

    def print_energy_changes(self, energy_changes: Dict[int, float]) -> None:
        """
        Print the energy changes for each reaction step and the step with the largest energy change.

        Args:
            energy_changes (dict): A dictionary where keys are integers (reaction steps) and
                values are floats (corresponding energy changes in eV).

        """
        # Print energy changes
        print("Energy Changes:")
        for step, energy in energy_changes.items():
            print(f"Step {step}: Energy Change = {energy:.4f} eV")

        # Print total energy change
        total_energy_change = sum(energy_changes.values())
        print(f"The total energy change is {total_energy_change:.4f} eV.")

        # Find and print the largest energy change
        largest_energy_change_step = max(energy_changes, key=energy_changes.get)
        largest_energy_change = energy_changes[largest_energy_change_step]
        print(f"Largest Energy Change: Step {largest_energy_change_step}, Energy Change = {largest_energy_change:.4f} eV")
