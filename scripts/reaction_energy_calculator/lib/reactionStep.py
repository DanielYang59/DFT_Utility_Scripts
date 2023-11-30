#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import warnings
from typing import Dict

def validate_species_dict(func):
    def wrapper(self, *args, **kwargs):
        # Check reactants and products dictionaries
        for dictionary in [self.reactants, self.products]:
            # Check stoichiometric numbers
            for value in dictionary.values():
                if not isinstance(value, int) or value <= 0:
                    raise ValueError("All values in reactants and products must be integers greater than 0.")

            # Check proton and hydroxide names
            if "h+" in dictionary.keys() or "oh-" in dictionary.keys():
                warnings.warn("Proton (H+) or hydroxide (OH-) names should be in all capital letters.")

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
    def set_reactants(self, reactants: Dict[str, int]) -> None:
        self.reactants = reactants

    @validate_species_dict
    def set_products(self, products: Dict[str, int]) -> None:
        self.products = products

    def calculate_free_energy_change(self) -> float:
        # TODO:

        return self.deltaG0
