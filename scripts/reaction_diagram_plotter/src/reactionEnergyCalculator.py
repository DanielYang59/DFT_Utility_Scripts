#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from pathlib import Path
from typing import Dict
import pandas as pd

class ReactionEnergyCalculator:
    def __init__(self, intermediate_energy_file: Path, species_energy_file: Path) -> None:
        # Import intermediate energies and species energies
        self.intermediate_energies = self._import_energy_csv_file(intermediate_energy_file)
        self.species_energies = self._import_energy_csv_file(species_energy_file)

    def _import_energy_csv_file(self, file: Path, energy_name: str = "free_energy") -> Dict[str, float]:
        """
        Import and parse energy data from a CSV file into a dictionary.

        Args:
            file (Path): Path to the CSV file containing energy data.

        Raises:
            FileNotFoundError: If the CSV file is not found or has an illegal extension.

        Returns:
            Dict[str, float]: A dictionary where keys are column names and values are energy values.
        """
        # Check if the file exists and has a ".csv" extension
        if not file.is_file() or file.suffix != ".csv":
            raise FileNotFoundError(f"Energy CSV file '{file}' not found or illegal.")

        # Import energy CSV file using pandas and convert to dictionary
        energy_data = pd.read_csv(file)
        return dict(zip(energy_data['name'], energy_data[energy_name]))

    def _check_reaction_pathway(self):
        """
        Check reaction pathways.
        # TODO:

        """
        pass

    def import_reaction_pathway(self, pathway_file: Path) -> None:
        """
        Import and parse a reaction pathway from a JSON file.

        Args:
            pathway_file (Path): Path to the reaction pathway JSON file.

        Raises:
            FileNotFoundError: If the JSON file is not found or has an illegal extension.

        Example JSON file format:
            {
                "name": "pathway_name",
                "comment": "Example pathway for reaction diagram plotter",
                "1": {
                    "reactants": {"*": 1, "CO2": 1, "H+": 1, "e-": 1},
                    "products": {"*COOH": 1}
                },
                ...
                "8": {
                    "reactants": {"*OH": 1, "H2O_l": 1, "CH4_g": 1, "H+": 1, "e-": 1},
                    "products": {"*": 1, "H2O_l": 2, "CH4_g": 1}
                }
            }

        Parses the JSON file and stores the reaction pathway in the 'self.reaction_pathway' attribute.
        Also checks the integrity of the reaction pathway using the '_check_reaction_pathway' method.
        """
        # Check reaction pathway file
        if not pathway_file.is_file() or pathway_file.suffix != ".json":
            raise FileNotFoundError(f"Reaction pathway JSON file '{pathway_file}' not found or illegal.")

        # Load and parse the reaction pathway JSON file
        with open(pathway_file, 'r', encoding="utf-8") as json_file:
            self.reaction_pathway = json.load(json_file)

        # Check reaction pathway
        self._check_reaction_pathway()

    def _calculate_free_energy_change_for_step(self, ) -> float:
        pass

    def calculate_free_energy_change(self) -> Dict[int, float]:
        pass

# Test area
if __name__ == "__main__":
    # Initiate reaction energy calculator
    calculator = ReactionEnergyCalculator(
        intermediate_energy_file=Path("../example_usage/example_intermediate_energies.csv"),
        species_energy_file=Path("../example_usage/example_species_energies.csv")
        )

    # Import reaction pathway
    calculator.import_reaction_pathway(pathway_file=Path("../example_usage/example_reaction_pathway.json"))

    # Calculator free energy changes
    calculator.calculate_free_energy_change()