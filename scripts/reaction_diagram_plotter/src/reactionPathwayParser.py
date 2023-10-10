#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from pathlib import Path
from typing import Dict
import pandas as pd

class ReactionPathwayParser:
    """
    A utility class for parsing and validating reaction pathway data from JSON files.

    Methods:
        __init__(self, energy_col_name: str = "free_energy") -> None:
            Initialize the ReactionPathwayParser instance.

        _import_energy_csv_file(file: Path) -> Dict[str, float]:
            Import and parse energy data from a CSV file into a dictionary.

        _extract_reaction_pathway(pathway_json_content: dict) -> dict:
            Extract and check reaction pathways from the given JSON content.

        import_reaction_pathway(pathway_file: Path) -> Dict[int, dict]:
            Import and parse a reaction pathway from a JSON file.

    Attributes:
        energy_col_name (str): Column name for energy values in the CSV file.
    """

    def __init__(self, energy_col_name: str = "free_energy") -> None:
        """
        Initialize the ReactionPathwayParser instance.

        Args:
            energy_col_name (str, optional): Column name for energy values in the CSV file. Defaults to "free_energy".

        Raises:
            TypeError: If energy_col_name is not a string.
        """
        if not isinstance(energy_col_name, str):
            raise TypeError(f"Expect type str for energy_col_name, got {type(energy_col_name)}.")
        self.energy_col_name = energy_col_name

    def _import_energy_csv_file(self, file: Path) -> Dict[str, float]:
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
        return dict(zip(energy_data['name'], energy_data[self.energy_col_name]))

    def _extract_reaction_pathway(self, pathway_json_content: dict) -> dict:
        """
        Extract and check reaction pathways from the given JSON content.

        Args:
            pathway_json_content (dict): JSON content containing reaction pathways.

        Returns:
            dict: Extracted reaction pathways with keys as integers and values as dictionaries.

        Raises:
            ValueError: If the JSON content does not follow the expected format.
        """
        extracted_pathways = {}
        current_reaction_key = None

        for key, value in pathway_json_content.items():
            # Check if the key is "name" or "comment"
            if key in ["name", "comment"]:
                # Metadata key, continue to the next iteration
                continue

            # Check if the key is a continuous integer
            try:
                reaction_key = int(key)
                if reaction_key <= 0:
                    raise ValueError("Reaction pathway keys must be positive integers.")
                if reaction_key in extracted_pathways:
                    raise ValueError("Duplicate reaction pathway key found.")

            except ValueError:
                raise ValueError("Invalid reaction pathway key found. Keys must be continuous integers.")

            # Assign the current reaction key
            current_reaction_key = reaction_key

            # Check the structure of the reaction pathway
            if not all(k in value and "reactants" in value and "products" in value for k in ["reactants", "products"]):
                raise ValueError(f"Invalid structure for reaction pathway {current_reaction_key}.")

            # Add the valid reaction pathway to the extracted_pathways dictionary
            extracted_pathways[current_reaction_key] = value

        if current_reaction_key is None:
            raise ValueError("No valid reaction pathways found.")

        return extracted_pathways

    def import_reaction_pathway(self, pathway_file: Path) -> Dict[int, dict]:
        """
        Import and parse a reaction pathway from a JSON file.

        Args:
            pathway_file (Path): Path to the reaction pathway JSON file.

        Raises:
            FileNotFoundError: If the JSON file is not found or has an illegal extension.

        Returns:
            Dict[int, dict]: Extracted and validated reaction pathways.

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

        Parses the JSON file and returns the validated reaction pathways.
        """
        # Check reaction pathway file
        if not pathway_file.is_file() or pathway_file.suffix != ".json":
            raise FileNotFoundError(f"Reaction pathway JSON file '{pathway_file}' not found or illegal.")

        # Load and parse the reaction pathway JSON file
        with open(pathway_file, 'r', encoding="utf-8") as json_file:
            reaction_pathway_content = json.load(json_file)

        # Extract and check reaction information
        return self._extract_reaction_pathway(reaction_pathway_content)

# Test area
if __name__ == "__main__":
    # Initiate reaction pathway parser
    parser = ReactionPathwayParser()

    # Import reaction pathway
    pathway = parser.import_reaction_pathway(pathway_file=Path("../example_usage/example_reaction_pathway.json"))
    print(pathway)
