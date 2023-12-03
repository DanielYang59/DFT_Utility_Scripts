#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import Dict, Union
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
                if not isinstance(value, Union[int, float]) or value <= 0:
                    raise ValueError(f"All values in {name} must be numbers greater than 0.")

            # Check proton and hydroxide names
            if "h+" in dictionary.keys() or "oh-" in dictionary.keys():
                raise RuntimeError(f"Proton (H+) or hydroxide (OH-) names in {name} should be in all capital letters.")

            # Check electron name
            if "E+" in dictionary.keys():
                raise RuntimeError(f"Electron (e-) name in {name} should be in lower case.")

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

    def __init__(self, temperature: float, pH: float, external_potential: float) -> None:
        """
        Initialize a ReactionStep instance.

        Args:
            temperature (float): Temperature of the reaction.
            pH (float): pH of the reaction.
            external_potential (float): External potential applied to the reaction.
        """
        # Check parameters conditions
        assert temperature >= 0 and isinstance(temperature, Union[float, int])
        assert 0 <= pH <= 14 and isinstance(pH, Union[float, int])
        assert isinstance(external_potential, Union[float, int])

        self.temperature = temperature
        self.pH = pH
        self.external_potential = external_potential

    # @validate_species_dict
    def set_reactants(self, reactants: Dict[str, Union[float, int]], reactant_energies: Dict[str, float]) -> None:
        """
        Set the reactants and their energies.

        Args:
            reactants (Dict[str, int]): Dictionary representing the reactants and their stoichiometric coefficients.
            reactant_energies (Dict[str, float]): Dictionary representing the energies of the reactants.
        """
        assert isinstance(reactants, dict) and isinstance(reactant_energies, dict) and reactants and reactant_energies
        self.reactants = reactants
        self.reactant_energies = reactant_energies

    # @validate_species_dict
    def set_products(self, products: Dict[str, Union[float, int]], product_energies: Dict[str, float]) -> None:
        """
        Set the products and their energies.

        Args:
            products (Dict[str, int]): Dictionary representing the products and their stoichiometric coefficients.
            product_energies (Dict[str, float]): Dictionary representing the energies of the products.
        """
        assert isinstance(products, dict) and isinstance(product_energies, dict) and products and product_energies
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
        total_energy = 0
        for s in species.keys():
            total_energy += species[s] * energy_dict[s]

        return total_energy

    def calculate_free_energy_change(self, verbose: bool = False) -> float:
        """
        Calculate the free energy change for the reaction.

        Returns:
            float: The calculated free energy change.
        """
        # Calculate reactants total energy
        reactants_total_energy = self._calculate_total_energy(self.reactants, self.reactant_energies)

        # Calculate products total energy
        products_total_energy = self._calculate_total_energy(self.products, self.product_energies)

        if verbose:
            print(f"Reactants energy {reactants_total_energy} eV, products energy {products_total_energy} eV.")

        return products_total_energy - reactants_total_energy

    def _count_species(self, species_dict: dict, name: str) -> Union[float, int]:
        """
        Count the number of species in given dict.

        Returns:
            float: The number of species
        """
        if name in species_dict:
            return species_dict[name]
        else:
            return 0

    def calculate_pH_correction(self) -> float:
        """
        Calculate the pH correction for the reaction step.

        The pH correction accounts for changes in the concentration of protons (H+) and hydroxide ions (OH-)
        between the reactants and products in a chemical reaction.

        Returns:
            float: The calculated pH correction.

        Raises:
            RuntimeError: If both protons (H+) and hydroxide ions (OH-) coexist in the reaction step,
                or if pH correction data is not available for the specified temperature.
        """
        # Calculate total number of proton(H+) and hydroxide(OH-)
        proton_count = self._count_species(self.products, "H+") - self._count_species(self.reactants, "H+")
        hydroxide_count = self._count_species(self.products, "OH-") - self._count_species(self.reactants, "OH-")

        # Reaction should not have H+ and OH- simultaneously (except for H2O dissociation)
        if proton_count != 0 and hydroxide_count != 0:
            raise RuntimeError("H+ and OH- should not coexist in reaction step.")

        # Proton(H+) exists
        elif proton_count != 0:
            return proton_count * ((Boltzmann / elementary_charge) * self.temperature * math.log(10, math.e) * self.pH)

        # Hydroxide(OH-) exists
        elif hydroxide_count != 0:
            # Ionic product for H2O at different temperatures: https://www.chemguide.co.uk/physical/acidbaseeqia/kw.html
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
        """
        Calculate the external potential correction for the reaction step.

        The external potential correction accounts for changes in the number of electrons (e-) between
        the reactants and products in a chemical reaction, multiplied by the external potential applied.

        Returns:
            float: The calculated external potential correction.

        Notes:
            The external potential correction is calculated as -neU, where 'n' is the change in the number
            of electrons (e-), 'e' is the elementary charge, and 'U' is the external potential applied.

        Returns:
            float: The calculated external potential correction.

        """
        # Calculate total number of electrons
        electron_count = self._count_species(self.products, "e-") - self._count_species(self.reactants, "e-")

        return -electron_count * self.external_potential  # -neU
