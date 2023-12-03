#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .reactionStep import ReactionStep

class ComputationalHydrogenElectrode(ReactionStep):
    """
    Class representing a computational hydrogen electrode in a chemical reaction.

    Additional Attributes:
        additional_attribute (str): An additional attribute for the computational hydrogen electrode.

    Additional Methods:
        additional_method(): An additional method for the computational hydrogen electrode.
    """

    def __init__(self, pH: float, external_potential: float, gaseous_hydrogen_free_energy: float = -6.8331816, liquid_water_free_energy: float = -14.116412) -> None:
        """
        Initialize a ComputationalHydrogenElectrode instance.

        Args:
            deltaG0 (float): Standard Gibbs free energy change for the reaction.
            temperature (float): Temperature of the reaction.
            pH (float): pH of the reaction.
            external_potential (float): External potential applied to the reaction.
            additional_attribute (str): An additional attribute for the computational hydrogen electrode.

        Notes:
            Gaseous hydrogen (H2_g) free energy with corrections
            gaseous_hydrogen_free_energy = -6.7665366 - 0.066645

            Liquid water (H2O_l) free energy with corrections
            # liquid_water_free_energy = -14.218641 + 0.016010  # calculated at pressure of 3534 Pa
            liquid_water_free_energy = -14.218641 + 0.102229  # calculated at pressure of 101325 Pa
        """
        # Initialize CHE at 298.15 K
        super().__init__(298.15, pH, external_potential)

        # Set species and species energies
        self.gaseous_hydrogen_free_energy = gaseous_hydrogen_free_energy
        self.liquid_water_free_energy = liquid_water_free_energy

        if gaseous_hydrogen_free_energy is None:
            # Load recommended molecular energies
            self.load_recommended_molecule_energies()

        self.set_reactants(reactants={"H+":1, "e-":1}, reactant_energies={"H+":0, "e-":0})
        self.set_products(products={"H2_g":0.5}, product_energies={"H2_g":self.gaseous_hydrogen_free_energy})

        # Calculate free energy change
        self.calculate_free_energy_change()

        # Calculate pH and external potential corrections
        pH_correction = self.calculate_pH_correction()
        external_potential_correction = self.calculate_external_potential_correction()

        # Add corrections to free energy change
        self.free_energy_change = self.free_energy_change + pH_correction + external_potential_correction

    def calculate_proton_free_energy(self) -> float:
        """
        Calculate the free energy of proton-electron pair
        including pH and external potential corrections.

        Note:
            From reaction (H+ + e-) --> 0.5* H2_g.

        Returns:
            float: The calculated proton-electron pair free energy with pH and external potential corrections.
        """
        assert self.gaseous_hydrogen_free_energy < 0, "Illegal gaseous hydrogen free energy."
        return 0.5 * self.gaseous_hydrogen_free_energy - self.free_energy_change

    def calculate_hydroxide_free_energy(self, water_association_free_energy: float = -0.828) -> float:
        """
        Calculate the free energy of hydroxide-electron pair
        including pH and external potential corrections.

        Note:
            From reaction (H+ + e-) + (OH- - e-) --> H2O_l.

        Returns:
            float: The calculated hydroxide-electron pair free energy with pH and external potential corrections.
        """
        assert water_association_free_energy < 0, "Please input water \"association\" energy, not dissociation."
        assert self.liquid_water_free_energy < 0, "Liquid water free energy is illegal."

        return self.liquid_water_free_energy - self.calculate_proton_free_energy() - water_association_free_energy

# Test area
if __name__ == "__main__":
    che = ComputationalHydrogenElectrode(pH=14, external_potential=0)
    che.load_recommended_molecule_energies()
    print("(H+ + e-) energy:", che.calculate_proton_free_energy())
    print("(OH- - e-) energy:", che.calculate_hydroxide_free_energy())
