#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pathlib import Path

from src.read_input import read_molecular_species_csv, read_intermediate_csv, read_reaction_data
from src.reactionCalculator import reactionCalculator
from src.diagramGenerator import ReactionDiagramGenerator

def main():
    """
    Main function to orchestrate the calculation and plotting of a reaction pathway diagram.

    1. Reads molecular, intermediate, and reaction pathway data.
    2. Initializes a reactionCalculator object with the read data.
    3. Calculates the free energy change for each step in the reaction pathway.
    4. Generates a diagram based on the calculated free energy changes.
    """
    # Initialize reaction calculator
    calculator = reactionCalculator(read_molecular_species_csv("data/molecular_species_energy.csv"),
                                    read_intermediate_csv("data/intermediate_energy.csv"),
                                    read_reaction_data("data/reaction.json"),
                                    )

    # Perform calculations
    deltaG_dict = calculator.interpret_reaction_pathway()

    # Generate diagram using the new class
    diagram_generator = ReactionDiagramGenerator(
        deltaG_dict,
        store_path=Path("output")/"reaction_diagram.png",
        )
    diagram_generator.generate()

if __name__ == "__main__":
    main()
