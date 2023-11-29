#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class ComputationalHydrogenElectrode:
    def __init__(self, temperature: float, pH: float, external_potential: float, hydrogen_free_energy: float) -> None:
        # Check and take attributes
        assert temperature >= 0
        assert 0 <= pH <= 14

        self.temperature = temperature
        self.pH = pH
        self.external_potential = external_potential

        # Check and take hydrogen (H2_g) free energy
        assert hydrogen_free_energy > 0
        self.hydrogen_free_energy = hydrogen_free_energy

    def _calculate_proton_energy(self) -> float:
        pass

    def _calculate_hydroxide_energy(self) -> float:
        pass

    def calculate(self, species:str) -> float:
        # Calculate proton energy
        if species == "H+":
            return self._calculate_proton_energy

        # Calculate hydroxide energy
        elif species == "OH-":
            return self._calculate_hydroxide_energy

        else:
            raise ValueError("Illegal species. Please select either H+ or OH-.")

# Test area
if __name__ == "__main__":
    pass
