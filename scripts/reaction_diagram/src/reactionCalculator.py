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

    def _check_reaction_consistency(self):
        """
        Check for consistency in reaction steps.
        1. The number of atoms should be the same on both sides of each reaction step.
        2. The number of atoms should be consistent across different reaction steps.
        """

        # Initialize a dictionary to store the number of each type of atom for the first reaction step
        initial_atoms_count = {}

        # Loop through each reaction step to check atom balance
        for step, step_data in self.reaction_data["reaction_steps"].items():

            # Initialize counters for the reactants and products in this step
            reactant_atoms_count = {}
            product_atoms_count = {}

            # Count atoms in reactants for this step
            for reactant, coefficient in step_data["reactants"].items():
                self._count_atoms(reactant, coefficient, reactant_atoms_count)

            # Count atoms in products for this step
            for product, coefficient in step_data["products"].items():
                self._count_atoms(product, coefficient, product_atoms_count)

            # Check if the number of atoms is the same on both sides of this reaction step
            if reactant_atoms_count != product_atoms_count:
                raise ValueError(f"Atom count mismatch in reaction step {step}. Reactants: {reactant_atoms_count}, Products: {product_atoms_count}")

            # For the first step, store the atom count for future comparisons
            if step == "step_1":
                initial_atoms_count = reactant_atoms_count
            else:
                # Check if the number of atoms is consistent across different reaction steps
                if initial_atoms_count != reactant_atoms_count:
                    raise ValueError(f"Atom count mismatch between reaction steps. Initial: {initial_atoms_count}, Current step {step}: {reactant_atoms_count}")

    def _count_atoms(self, species: str, coefficient: int, atom_count_dict: dict):
        """
        Count the number of atoms in a given species and update the atom count dictionary.

        Parameters:
            species (str): The chemical species.
            coefficient (int): The stoichiometric coefficient for this species in the reaction.
            atom_count_dict (dict): The current count of atoms, which will be updated.

        Returns:
            None: The atom_count_dict will be updated in place.
        """
        # Ignore clean catalyst surface
        if species == "*":
            return

        # Handle PEP special case
        if species == "PEP":
            atom_count_dict["H"] = atom_count_dict.get("H", 0) + 1 * coefficient
            return

        # Handle adsorbed species
        if species.startswith("*"):
            species = species[1:]

        # Handle free species with state (e.g., H2O_l, CO2_g)
        if "_" in species:
            species = species.split("_")[0]

        # Count atoms in the cleaned-up species string
        current_char = ""
        current_count = ""
        for char in species:
            if char.isalpha():
                # Save the count of the previous atom
                if current_char and current_count:
                    atom_count_dict[current_char] = atom_count_dict.get(current_char, 0) + int(current_count) * coefficient
                # Start counting a new atom
                current_char = char
                current_count = "1"  # Default count is 1
            elif char.isnumeric():
                current_count = char  # Override the default count

        # Save the count of the last atom in the string
        if current_char and current_count:
            atom_count_dict[current_char] = atom_count_dict.get(current_char, 0) + int(current_count) * coefficient
