#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import Dict

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
    def __init__(self, deltaG0: float, temperature: float, pH: float, external_potential: float) -> None:
        # Check external conditions
        assert temperature >= 0
        assert 0 <= pH <= 14

        self.deltaG0 = deltaG0
        self.temperature = temperature
        self.pH = pH
        self.external_potential = external_potential

        self.reactants = {}
        self.products = {}

    @validate_species_dict
    def set_reactants(self, reactants: Dict[str, int], reactant_energies: Dict[str, float]) -> None:
        assert reactants
        self.reactants = reactants
        self.reactant_energies = reactant_energies

    @validate_species_dict
    def set_products(self, products: Dict[str, int], product_energies: Dict[str, float]) -> None:
        assert products
        self.products = products
        self.product_energies = product_energies

    def calculate_free_energy_change(self) -> float:


        return self.deltaG0
