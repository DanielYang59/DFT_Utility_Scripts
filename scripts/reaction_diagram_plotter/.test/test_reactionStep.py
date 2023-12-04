#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Test objectives: Test the results of reactionSteps and compare them to manual calculations.

Target Reaction One: H+ + e- --> 0.5 * H2_g for the following ΔGs:
    a. pH = 0, U = 0 (expect 0)
    b. pH = 7, U = 0 (expect -0.4144)
    d. pH = 0, U = 1 (expect 1)
    e. pH = 0, U = -1 (expect -1)
    f. pH = 7, U = 1 (expect 1-0.4144=0.5856)

Target Reaction Two: 0.5 * H2_g --> H+ + e- for the following ΔGs:
    (Expect reverses of Target One)
    a'. pH = 0, U = 0
    b'. pH = 7, U = 0
    d'. pH = 0, U = 1
    e'. pH = 0, U = -1
    f'. pH = 7, U = 1

Target Reaction Three: H2O_l --> 0.5 * H2_g + OH- - e- for the following ΔGs:
    a. pH = 14, U = 0 (expect ΔGw=0.822 eV)
    b. pH = 7, U = 0 (expect X)
    c. pH = 14, U = 1 (expect X)
"""

import sys
import os

# Append the 'src' directory to the Python path
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'src'))

# Now you can import modules from 'src'
from reactionStep import ReactionStep

# Set up global temperature
temperature = 298.15

def test_reaction_one():
    # Define reactions and products
    reactants = {"H+": 1, "e-": 1}
    reactant_energies = {"H+": -3.3836, "e-": 0}  # NOTE: manual energy setup of proton-electron pair
    products = {"H2_g": 0.5}
    product_energies = {"H2_g": -6.7672}

    # Set up condition a
    step_a = ReactionStep(temperature=temperature, pH=0, external_potential=0)
    step_a.set_reactants(reactants, reactant_energies)
    step_a.set_products(products, product_energies)
    print("Reaction One: Step a:" ,step_a.calculate_free_energy_change())

    # Set up condition b
    step_b = ReactionStep(temperature=temperature, pH=7, external_potential=0)
    step_b.set_reactants(reactants, reactant_energies)
    step_b.set_products(products, product_energies)
    print("Reaction One: Step b:" ,step_b.calculate_free_energy_change())

    # Set up condition c
    step_c = ReactionStep(temperature=temperature, pH=0, external_potential=1)
    step_c.set_reactants(reactants, reactant_energies)
    step_c.set_products(products, product_energies)
    print("Reaction One: Step c:" ,step_c.calculate_free_energy_change())

    # Set up condition d
    step_d = ReactionStep(temperature=temperature, pH=0, external_potential=-1)
    step_d.set_reactants(reactants, reactant_energies)
    step_d.set_products(products, product_energies)
    print("Reaction One: Step d:" ,step_d.calculate_free_energy_change())

    # Set up condition e
    step_e = ReactionStep(temperature=temperature, pH=7, external_potential=1)
    step_e.set_reactants(reactants, reactant_energies)
    step_e.set_products(products, product_energies)
    print("Reaction One: Step e:" ,step_e.calculate_free_energy_change())

def test_reaction_two():
    # Define reactions and products
    reactants = {"H2_g": 0.5}
    reactant_energies = {"H2_g": -6.7672}
    products = {"H+": 1, "e-": 1}
    product_energies = {"H+": -3.3836, "e-": 0}  # NOTE: manual energy setup of proton-electron pair

    # Set up condition a
    step_a = ReactionStep(temperature=temperature, pH=0, external_potential=0)
    step_a.set_reactants(reactants, reactant_energies)
    step_a.set_products(products, product_energies)
    print("Reaction Two: Step a:" ,step_a.calculate_free_energy_change())

    # Set up condition b
    step_b = ReactionStep(temperature=temperature, pH=7, external_potential=0)
    step_b.set_reactants(reactants, reactant_energies)
    step_b.set_products(products, product_energies)
    print("Reaction Two: Step b:" ,step_b.calculate_free_energy_change())

    # Set up condition c
    step_c = ReactionStep(temperature=temperature, pH=0, external_potential=1)
    step_c.set_reactants(reactants, reactant_energies)
    step_c.set_products(products, product_energies)
    print("Reaction Two: Step c:" ,step_c.calculate_free_energy_change())

    # Set up condition d
    step_d = ReactionStep(temperature=temperature, pH=0, external_potential=-1)
    step_d.set_reactants(reactants, reactant_energies)
    step_d.set_products(products, product_energies)
    print("Reaction Two: Step d:" ,step_d.calculate_free_energy_change())

    # Set up condition e
    step_e = ReactionStep(temperature=temperature, pH=7, external_potential=1)
    step_e.set_reactants(reactants, reactant_energies)
    step_e.set_products(products, product_energies)
    print("Reaction Two: Step e:" ,step_e.calculate_free_energy_change())

def test_reaction_three():
    # Define reactions and products
    reactants = {"H2O_l": 1, "e-":1}
    reactant_energies = {"H2O_l": -14.22, "e-": 0}
    products = {"H2_g": 0.5, "OH-": 1}
    product_energies = {"H2_g": -6.7672, "OH-": -10.0082}  # NOTE: manual energy setup of hydroxide-electron pair

    # Set up condition a
    step_a = ReactionStep(temperature=temperature, pH=14, external_potential=0)
    step_a.set_reactants(reactants, reactant_energies)
    step_a.set_products(products, product_energies)
    print("Reaction Three: Step a:" ,step_a.calculate_free_energy_change())

    # Set up condition b
    step_b = ReactionStep(temperature=temperature, pH=7, external_potential=0)
    step_b.set_reactants(reactants, reactant_energies)
    step_b.set_products(products, product_energies)
    print("Reaction Three: Step b:" ,step_b.calculate_free_energy_change())

    # Set up condition c
    step_c = ReactionStep(temperature=temperature, pH=14, external_potential=1)
    step_c.set_reactants(reactants, reactant_energies)
    step_c.set_products(products, product_energies)
    print("Reaction Three: Step c:" ,step_c.calculate_free_energy_change())

if __name__ == "__main__":
    test_reaction_one()

    test_reaction_two()

    test_reaction_three()
