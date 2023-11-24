#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import Union, Dict
from scipy.constants import Boltzmann, elementary_charge
import math

from .energyReader import EnergyReader

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

    def _calculate_half_reaction_energy(self, species: Dict[str, int]) -> float:
        """
        Calculate the half reaction energy based on the given species and their stoichiometric numbers.

        Args:
            species (Dict[str, int]): A dictionary where keys are species names and values are stoichiometric numbers.

        Returns:
            float: The calculated half reaction energy in the specified energy units.

        Raises:
            TypeError: If the species name is not a string.
            ValueError: If the stoichiometric number is not a positive integer or if the species type is unrecognizable.

        Calculates the half reaction energy by summing the contributions from each species in the reaction. The species
        names are used to identify the type of species (electron, ion, molecule, or reaction intermediate). The stoichiometric
        numbers determine the quantity of each species in the reaction. The resulting energy is returned in the specified
        energy units.
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
            ## Electron energy (ignore)
            if name == "e-":
                pass

            ## Proton energy (with Computational Hydrogen Electrode method)
            elif name == "H+":
                proton_energy = 0.5 * self.energy_reader.read_molecule_or_ion_energy("H2_g")
                energy += num * proton_energy

            ## Species is "ion" or "molecule"
            elif name.endswith("-") or name.endswith("+") or name.endswith("_g") or name.endswith("_l"):
                species_energy = self.energy_reader.read_molecule_or_ion_energy(name)
                energy += num * species_energy

            ## Species is "reaction intermediate"
            elif name.startswith("*"):
                species_energy = self.energy_reader.read_intermediate_energy(name)
                energy += num * species_energy

            ## Unrecognizable species type
            else:
                raise ValueError(f"Unrecognizable species type for '{name}'.")

        return energy

    def _calculate_energy_change_for_step(self, pathway: dict) -> tuple:
        """
        Calculate the energy change for a given reaction step based on the provided pathway details.

        Args:
            pathway (dict): A dictionary containing 'reactants' and 'products' keys, each with their respective components.

        Returns:
            (float, float): The total energies of (products, reactants).

        """
        # Calculate energy for products
        products_energy = self._calculate_half_reaction_energy(pathway["products"])

        # Calculate energy for reactants
        reactants_energy = self._calculate_half_reaction_energy(pathway["reactants"])

        return products_energy, reactants_energy

    def _calculate_net_species_count(self, reaction_pathway: dict, species_name: str) -> int:
        """
        Calculate the net count of a specific chemical species in a reaction pathway.

        Parameters:
        - reaction_pathway (dict): A dictionary representing the reaction pathway with "products" and "reactants".
        - species_name (str): The name of the chemical species for which the net count is calculated.

        Returns:
        - int: The net count of the specified species in the reaction pathway.

        The function extracts the counts of the specified species from both products and reactants
        in the given reaction pathway and calculates the net count by subtracting the reactant count
        from the product count.

        """
        # Extract species
        products = reaction_pathway["products"]
        reactants = reaction_pathway["reactants"]

        net_count = 0

        # Calculate species count in products
        if species_name in products:
            net_count += products[species_name]

        # Calculate species count in reactants
        if species_name in reactants:
            net_count -= reactants[species_name]

        return net_count

    def _add_energy_corrections(self, reaction_pathway: dict, energy_change: float) -> float:
        """
        Add energy corrections to the total energy change based on external potential and pH.

        Parameters:
        - reaction_pathway (dict): A dictionary representing the reaction pathway with "products" and "reactants".
        - energy_change (float): The original energy change associated with the reaction.

        Returns:
        - float: The total energy change with external potential and pH corrections.

        This function calculates two types of energy corrections:
        1. External potential correction: Accounts for the contribution of electrons to an external potential.
        2. pH correction: Adjusts the energy change based on the imbalance of protons (H+) and hydroxide ions (OH-).

        The external potential correction is calculated by multiplying the net electron count by the external potential.
        The pH correction is calculated based on the difference between the net counts of protons and hydroxide ions.
        If both protons and hydroxide ions are present, a RuntimeError is raised since they should not coexist in a reaction.

        """
        # Calculate external potential correction
        net_electron_count = self._calculate_net_species_count(reaction_pathway, "e-")
        potential_correction = -net_electron_count * self.external_potential  # -neU

        # Calculate pH correction (based on H+ and OH- numbers)
        net_proton_count = self._calculate_net_species_count(reaction_pathway, "H+")
        net_hydroxide_count = self._calculate_net_species_count(reaction_pathway, "OH-")

        ## Check H+ and OH- count
        if net_proton_count == 0 and net_hydroxide_count == 0:
            pH_correction = 0

        elif net_proton_count == 0 or net_hydroxide_count == 0:
            pH_correction = (net_proton_count - net_hydroxide_count) * ((Boltzmann / elementary_charge) * self.temperature * math.log(10, math.e) * self.pH)  # DEBUG: need double check

        else:
            raise RuntimeError("Reaction equation should not have H+ and OH- simultaneously.")

        return energy_change + potential_correction + pH_correction

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
            # Calculate products and reactants energies
            products_energy, reactants_energy = self._calculate_energy_change_for_step(pathway)

            # Calculate energy change
            energy_change = products_energy - reactants_energy

            # Add external potential and pH corrections
            energy_changes[index] = self._add_energy_corrections(pathway, energy_change)

            # Verbose
            if self.verbose:
                print(f"Step {index}: product_energy {products_energy:.4f} eV, reactant_energy {reactants_energy:.4f} eV.")

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
