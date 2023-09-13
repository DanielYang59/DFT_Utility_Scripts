#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class reactionCalculator:
    def __init__(self, molecular_energy: dict, intermediate_energy: dict, reaction_data: dict):
        """
        Initialize the reactionCalculator object.

        Parameters:
            molecular_energy (dict): Energy data for molecular species.
            intermediate_energy (dict): Energy data for reaction intermediates.
            reaction_data (dict): Reaction pathway and external conditions.
        """
        self.molecular_energy = molecular_energy
        self.intermediate_energy = intermediate_energy
        self.reaction_data = reaction_data

        # Parse calculation conditions
        self.equilibrium_potential_V = reaction_data["Intrinsic_Properties"]["equilibrium_potential_V"]
        self.ph = reaction_data["External_Conditions"]["ph"]
        self.applied_potential = reaction_data["External_Conditions"]["applied_potential"]
        self.target_temperature = reaction_data["External_Conditions"]["target_temperature"]

    def interpret_reaction_pathway(self) -> dict:
        """
        Interpret and calculate the reaction energies for each step in the pathway.

        Returns:
            dict: A dictionary containing free energy changes for each step.
        """
        reaction_steps = self.reaction_data["Intrinsic_Properties"]["Reaction_Steps"]
        free_energy_changes = {}

        for step, values in reaction_steps.items():
            reactant_energy = self._calculate_free_energy(values["reactants"])
            product_energy = self._calculate_free_energy(values["products"])

            # Calculate free energy change of selected reaction step
            free_energy_changes[step] = product_energy - reactant_energy

        return free_energy_changes

    def _calculate_free_energy(self, species_dict: dict) -> float:
        """
        Calculate the free energy for a set of species.

        Parameters:
            species_dict (dict): Dictionary containing species and their respective coefficients.

        Returns:
            float: The calculated free energy.
        """
        total_energy = 0.0

        for species, coefficient in species_dict.items():
            # Check if stoichiometric coefficient is integer
            if not isinstance(coefficient, int) or coefficient <= 0:
                raise ValueError(f"The stoichiometric coefficient for species {species} must be an integer greater than zero.")

            # Calculate the energy of each species
            if species == "*":  # clean catalyst surface
                pass

            elif species == "PEP":  # proton-electron pairs
                pep_energy = 0.5 * self.molecular_energy["H2"] - self.applied_potential
                total_energy += (coefficient * pep_energy)

            elif species.startswith("*"):  # adsorbed species (*CO2 for example)
                if species in self.intermediate_energy:
                    ads_species_energy = self.intermediate_energy[species]
                    total_energy += (coefficient * ads_species_energy)
                else:
                    raise KeyError(f"Cannot find energy entry for {species} in intermediate_energy.csv.")

            else:  # non-adsorbed (free) species (H2O_l for example)
                if species in self.molecular_energy:
                    mol_species_energy = self.intermediate_energy[species]
                    total_energy += (coefficient * mol_species_energy)
                else:
                    raise KeyError(f"Cannot find energy entry for {species} in molecular_species_energy.csv.")

        return total_energy
