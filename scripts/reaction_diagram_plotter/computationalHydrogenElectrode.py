#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Notes:
    Gaseous hydrogen (H2_g) free energy with corrections
    gaseous_hydrogen_free_energy = -6.7665366 - 0.066645

    Liquid water (H2O_l) free energy with corrections
    # liquid_water_free_energy = -14.218641 + 0.016010  # calculated at pressure of 3534 Pa
    liquid_water_free_energy = -14.218641 + 0.102229  # calculated at pressure of 101325 Pa
"""
gasesous_hydrogen_free_energy = -6.8331816
liquid_water_free_energy = -14.116412

from src.reactionStep import ReactionStep

class ComputationalHydrogenElectrode:
    """
    Class representing a computational hydrogen electrode (CHE).
    """

    def __init__(self, pH: float, external_potential: float, temperature: float = 298.15, gaseous_hydrogen_free_energy: float = gasesous_hydrogen_free_energy, liquid_water_free_energy: float = liquid_water_free_energy) -> None:
        """
        Initialize a ComputationalHydrogenElectrode instance.

        Args:
            pH (float): pH of the reaction.
            external_potential (float): External potential applied to the reaction.
            temperature (float): Temperature in Kevin of the reaction.
            gaseous_hydrogen_free_energy (float): free energy of H2_g
            liquid_water_free_energy (float): free energy of H2O_l
        """
        # Initialize CHE at 298.15 K
        che = ReactionStep(temperature, pH, external_potential)

        # Set species and species energies
        self.gaseous_hydrogen_free_energy = gaseous_hydrogen_free_energy
        self.liquid_water_free_energy = liquid_water_free_energy

        # Set up reaction: H+ + e- --> 0.5 * H2_g
        che.set_reactants(reactants={"H+":1, "e-": 1}, reactant_energies={"H+":0, "e-": 0})
        che.set_products(products={"H2_g":0.5}, product_energies={"H2_g":0})

        # Calculate free energy change
        self.free_energy_change = che.calculate_free_energy_change()

        # Take temperature
        self.temperature = temperature

    def calculate_proton_free_energy(self) -> float:
        """
        Calculate the free energy of proton-electron pair
        including pH and external potential corrections.

        Note:
            From reaction (H+ + e-) --> 0.5* H2_g.

        Returns:
            float: The calculated proton-electron pair free energy with pH and external potential corrections.
        """
        assert self.gaseous_hydrogen_free_energy < 0, "Illegal gaseous hydrogen free energy, should be negative."
        return 0.5 * self.gaseous_hydrogen_free_energy - self.free_energy_change

    def calculate_hydroxide_free_energy(self) -> float:
        """
        Calculate the free energy of hydroxide-electron pair
        including pH and external potential corrections.

        Note:
            From reaction (H+ + e-) + (OH- - e-) --> H2O_l.

        Returns:
            float: The calculated hydroxide-electron pair free energy with pH and external potential corrections.
        """
        # Get water dissociation/association energy at given temperature
        water_association_free_energies = {298.15: -0.828}  # TODO: add data for other temperatures

        if self.temperature in water_association_free_energies.keys():
            assert self.liquid_water_free_energy < 0, "Liquid water free energy is illegal, should be negative."
            return self.liquid_water_free_energy - self.calculate_proton_free_energy() - water_association_free_energies[self.temperature]

        else:
            raise RuntimeError(f"Currently don't have water dissociation energy for temperature {self.temperature} K.")

def main():
    # Get user input for pH, external potential, and temperature
    pH = float(input("Enter the pH: "))
    external_potential = float(input("Enter the external potential: "))
    temperature = float(input("Enter the temperature in Kelvin: "))

    # Create ComputationalHydrogenElectrode object with user-input values
    che = ComputationalHydrogenElectrode(pH=pH, external_potential=external_potential, temperature=temperature)

    # Print the results of the calculations
    print(f"Proton-electron pair Free Energy: {che.calculate_proton_free_energy():.4f} eV.", )
    print(f"Hydroxide-electron pair Free Energy: {che.calculate_hydroxide_free_energy():.4f} eV.")

if __name__ == "__main__":
    main()
