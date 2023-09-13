#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from src.read_input import read_molecular_energy, read_intermediate_energy, read_reaction_data
from src.reactionCalculator import reactionCalculator
from src.generate_diagram import generate_reaction_diagram

def main():
    # Initialize reaction calculator
    calculator = reactionCalculator(read_molecular_energy("data/molecular_energy.csv"),
                                    read_intermediate_energy("data/intermediate_energy.csv"),
                                    read_reaction_data("data/reaction.json"),
                                    )

    # Perform calculations
    deltaG_dict = calculator.interpret_reaction_pathway()

    # Generate diagram
    generate_reaction_diagram(deltaG_dict)

if __name__ == "__main__":
    main()
