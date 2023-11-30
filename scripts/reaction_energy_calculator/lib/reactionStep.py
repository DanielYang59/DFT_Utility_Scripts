#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import Dict, Union
from functools import reduce
from scipy.constants import Boltzmann, elementary_charge
import math

def validate_species_dict(func):
    """
    Decorator to validate species dictionaries and their corresponding energy dictionaries.

    This decorator checks that the values in species dictionaries (reactants and products)
    are integers greater than 0, proton (H+) or hydroxide (OH-) names are in all capital letters,
    and keys in species dictionaries match keys in energy dictionaries (reactant_energies and product_energies).

    Args:
        func (callable): The function to be decorated.

    Returns:
        callable: The decorated function.
    """
    def wrapper(self, *args, **kwargs):
        # Parse dicts
        reactants, reactant_energies = args[0].get('reactants', {}), args[0].get('reactant_energies', {})
        products, product_energies = args[0].get('products', {}), args[0].get('product_energies', {})

        # Check reactants and products dictionaries
        for dictionary, energy_dict, name in [(reactants, reactant_energies, 'Reactants'), (products, product_energies, 'Products')]:
            # Check stoichiometric numbers
            for value in dictionary.values():
                if not isinstance(value, int) or value <= 0:
                    raise ValueError(f"All values in {name} must be integers greater than 0.")

            # Check proton and hydroxide names
            if "h+" in dictionary.keys() or "oh-" in dictionary.keys():
                raise RuntimeError(f"Proton (H+) or hydroxide (OH-) names in {name} should be in all capital letters.")

            # Check keys match between species and energies
            if set(dictionary.keys()) != set(energy_dict.keys()):
                raise ValueError(f"Keys of {name} and {name} energies must match.")

        return func(self, *args, **kwargs)
    return wrapper

class ReactionStep:
    """
    Class representing a step in a chemical reaction.

    Attributes:
        deltaG0 (float): Standard Gibbs free energy change for the reaction.
        temperature (float): Temperature of the reaction.
        pH (float): pH of the reaction.
        external_potential (float): External potential applied to the reaction.

        reactants (Dict[str, int]): Dictionary representing the reactants and their stoichiometric coefficients.
        reactant_energies (Dict[str, float]): Dictionary representing the energies of the reactants.

        products (Dict[str, int]): Dictionary representing the products and their stoichiometric coefficients.
        product_energies (Dict[str, float]): Dictionary representing the energies of the products.

        free_energy_change (float): free energy change of reaction step.
    """

    def __init__(self, deltaG0: float, temperature: float, pH: float, external_potential: float) -> None:
        """
        Initialize a ReactionStep instance.

        Args:
            deltaG0 (float): Standard Gibbs free energy change for the reaction.
            temperature (float): Temperature of the reaction.
            pH (float): pH of the reaction.
            external_potential (float): External potential applied to the reaction.
        """
        # Check parameters conditions
        assert temperature >= 0 and isinstance(temperature, Union(float, int))
        assert 0 <= pH <= 14 and isinstance(pH, Union(float, int))
        assert isinstance(deltaG0, Union(float, int))
        assert isinstance(external_potential, Union(float, int))

        self.deltaG0 = deltaG0
        self.temperature = temperature
        self.pH = pH
        self.external_potential = external_potential

    @validate_species_dict
    def set_reactants(self, reactants: Dict[str, int], reactant_energies: Dict[str, float]) -> None:
        """
        Set the reactants and their energies.

        Args:
            reactants (Dict[str, int]): Dictionary representing the reactants and their stoichiometric coefficients.
            reactant_energies (Dict[str, float]): Dictionary representing the energies of the reactants.
        """
        assert isinstance(reactants, Dict[str, int]) and isinstance(reactant_energies, Dict[str, float]) and reactants and reactant_energies
        self.reactants = reactants
        self.reactant_energies = reactant_energies

    @validate_species_dict
    def set_products(self, products: Dict[str, int], product_energies: Dict[str, float]) -> None:
        """
        Set the products and their energies.

        Args:
            products (Dict[str, int]): Dictionary representing the products and their stoichiometric coefficients.
            product_energies (Dict[str, float]): Dictionary representing the energies of the products.
        """
        assert isinstance(products, Dict[str, int]) and isinstance(product_energies, Dict[str, float]) and products and product_energies
        self.products = products
        self.product_energies = product_energies

    def _calculate_total_energy(self, species: Dict[str, int], energy_dict: Dict[str, float]) -> float:
        """
        Calculate the total energy for a given set of species.

        Args:
            species (Dict[str, int]): Dictionary representing the species and their stoichiometric coefficients.
            energy_dict (Dict[str, float]): Dictionary representing the energies of the species.

        Returns:
            float: The total energy for the specified species.
        """
        return reduce(lambda accumulator, species_name: accumulator + species[species_name] * energy_dict[species_name], species, 0)

    def calculate_free_energy_change(self) -> None:
        """
        Calculate the free energy change for the reaction.

        Returns:
            float: The calculated free energy change.
        """
        # Calculate reactants total energy
        reactants_total_energy = self._calculate_total_energy(self.reactants, self.reactant_energies)

        # Calculate products total energy
        products_total_energy = self._calculate_total_energy(self.products, self.product_energies)

        self.free_energy_change = products_total_energy - reactants_total_energy

    def calculate_pH_correction(self) -> float:
        # Calculate total number of proton(H+) and hydroxide(OH-)
        proton_count = self.products["H+"] - self.reactants["H+"]
        hydroxide_count = self.products["OH-"] - self.reactants["OH-"]

        # Reaction should not have H+ and OH- simultaneously (except for H2O dissociation)
        if proton_count != 0 and hydroxide_count != 0:
            raise RuntimeError("H+ and OH- should not coexist in reaction step.")

        # Proton(H+) exists
        elif proton_count != 0:
            return proton_count * ((Boltzmann / elementary_charge) * self.temperature * math.log(10, math.e) * self.pH)

        # Hydroxide(OH-) exists
        elif hydroxide_count != 0:
            # Ionic product for H2O at different temperature: https://www.chemguide.co.uk/physical/acidbaseeqia/kw.html
            kw_at_diff_temp = {273.15: 0.114 * (10 ** -14), 283.15: 0.293 * (10 ** -14), 293.15: 0.681 * (10 ** -14), 298.15: 1.008 * (10 ** -14), 303.15: 1.471 * (10 ** -14), 313.15: 2.916 * (10 ** -14), 323.15: 5.476 * (10 ** -14), 373.15: 51.3 * (10 ** -14)}

            if self.temperature in kw_at_diff_temp:
                pOH = -math.log(kw_at_diff_temp[self.temperature], 10) - self.pH
            else:
                raise RuntimeError(f"Don't have pH correction data for temperature {self.temperature} K. Available temperatures: {kw_at_diff_temp.keys()}")

            return hydroxide_count * ((Boltzmann / elementary_charge) * self.temperature * math.log(10, math.e) * pOH)

        # If no H+ and OH- at all, not pH dependent
        else:
            return 0

    def calculate_external_potential_correction(self) -> float:
        pass
