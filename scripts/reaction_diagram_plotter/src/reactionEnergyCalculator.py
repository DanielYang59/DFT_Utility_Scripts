#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import Union, Dict

class ReactionEnergyCalculator:
    """
    TODO:
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
            (float, float): The total energies of (products, reactants).

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
        energy_change = {}
        for index, pathway in self.reaction_pathways.items():
            # Calculate products and reactants energies
            products_energy, reactants_energy = self._calculate_energy_change_for_step(pathway)

            # Calculate energy change
            energy_change[index] = products_energy - reactants_energy

            # Verbose
            if self.verbose:
                print(f"Step {index + 1}: product_energy {products_energy} eV, reaction")

        return energy_change

# Test area
if __name__ == "__main__":
    # Import reaction pathway
    pathway = {1: {'reactants': {'*': 1, 'CO2': 1, 'H+': 1, 'e-': 1}, 'products': {'*COOH': 1}}, 2: {'reactants': {'*COOH': 1, 'H+': 1, 'e-': 1}, 'products': {'*CO': 1, 'H2O_l': 1}}, 3: {'reactants': {'*CO': 1, 'H2O_l': 1, 'H+': 1, 'e-': 1}, 'products': {'*CHO': 1, 'H2O_l': 1}}, 4: {'reactants': {'*CHO': 1, 'H2O_l': 1, 'H+': 1, 'e-': 1}, 'products': {'*CH2O': 1, 'H2O_l': 1}}, 5: {'reactants': {'*CH2O': 1, 'H2O_l': 1, 'H+': 1, 'e-': 1}, 'products': {'*OCH3': 1, 'H2O_l': 1}}, 6: {'reactants': {'*OCH3': 1, 'H2O_l': 1, 'H+': 1, 'e-': 1}, 'products': {'*O': 1, 'H2O_l': 1, 'CH4_g': 1}}, 7: {'reactants': {'*O': 1, 'H2O_l': 1, 'CH4_g': 1, 'H+': 1, 'e-': 1}, 'products': {'*OH': 1, 'H2O_l': 1, 'CH4_g': 1}}, 8: {'reactants': {'*OH': 1, 'H2O_l': 1, 'CH4_g': 1, 'H+': 1, 'e-': 1}, 'products': {'*': 1, 'H2O_l': 2, 'CH4_g': 1}}}

    # Initiate reaction energy calculator
    calculator = ReactionEnergyCalculator(
        external_potential=0
        )

    calculator.calculate_energy_change(pathway)
