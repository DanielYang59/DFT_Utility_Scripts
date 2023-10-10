#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import Union, Dict
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

    def __init__(self, external_potential: Union[float, int] = 0, pH: Union[float, int] = 7, verbose: bool = True) -> None:
        """
        Initialize the class instance with external potential and pH.

        Args:
            external_potential (Union[float, int], optional): External potential in volts. Defaults to 0.
            pH (Union[float, int], optional): pH value (0 to 14). Defaults to 7.
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
            # Species is "PEP (proton electron pair)"
            if name == "PEP":
                pep_energy = 0.5 * self.energy_reader.read_molecule_or_ion_energy("H2_g")
                energy -= num * self.external_potential  # -neU
                energy += num * pep_energy

            # Species is "ion" or "molecule"
            elif name.endswith("-") or name.endswith("+") or name.endswith("_g") or name.endswith("_l"):
                species_energy = self.energy_reader.read_molecule_or_ion_energy(name)
                energy += num * species_energy

            # Species is "reaction intermediate"
            elif name.startswith("*"):
                species_energy = self.energy_reader.read_intermediate_energy(name)
                energy += num * species_energy

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
            (float, float): The total energies of (products, reactants).

        """
        # Calculate energy for products
        products_energy = self._calculate_half_reaction_energy(pathway["products"])

        # Calculate energy for reactants
        reactants_energy = self._calculate_half_reaction_energy(pathway["reactants"])

        return products_energy, reactants_energy

    def calculate_energy_change(self, reaction_pathways: Dict[int, dict], energy_reader: EnergyReader) -> Dict[int, float]:
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

        # Check and take energy reader
        if not isinstance(energy_reader, EnergyReader):
            raise ValueError("Illegal data type for energy reader.")
        self.energy_reader = energy_reader

        # Calculate energy change for each reaction step
        energy_change = {}
        for index, pathway in self.reaction_pathways.items():
            # Calculate products and reactants energies
            products_energy, reactants_energy = self._calculate_energy_change_for_step(pathway)

            # Calculate energy change
            energy_change[index] = products_energy - reactants_energy

            # Verbose
            if self.verbose:
                print(f"Step {index}: product_energy {products_energy} eV, reactant_energy {reactants_energy} eV.")

        return energy_change

# Test area
if __name__ == "__main__":
    from pathlib import Path

    # Import reaction pathway
    from reactionPathwayParser import ReactionPathwayParser
    parser = ReactionPathwayParser()
    pathway = parser.import_reaction_pathway(Path("../example_usage/example_reaction_pathway.json"))

    # Initiate reaction energy calculator
    from pathlib import Path
    energy_reader = EnergyReader(
        intermediate_energy_file=Path("../example_usage/example_intermediate_energies.csv"),
        species_energy_file=Path("../example_usage/example_species_energies.csv")
        )
    calculator = ReactionEnergyCalculator(
        external_potential=0
        )

    calculator.calculate_energy_change(pathway, energy_reader)
