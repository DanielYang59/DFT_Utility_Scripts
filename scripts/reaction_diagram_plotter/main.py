#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
from pathlib import Path

from src.reactionPathwayParser import ReactionPathwayParser
from src.energyReader import EnergyReader
from src.reactionEnergyCalculator import ReactionEnergyCalculator
from src.diagramPlotter import DiagramPlotter

def main():
    # Get external potential and pH from argument
    external_potential, pH = parse_command_line_arguments()
    print(f"Working on external potential {external_potential} V and pH {pH}.")

    # Import reaction pathway
    pathway_parser = ReactionPathwayParser()
    reaction_pathways = pathway_parser.import_reaction_pathway(pathway_file=Path("reaction_pathway.json"))

    # Initiate energy reader
    energy_reader = EnergyReader(
        intermediate_energy_file=Path("intermediate_energies.csv"),
        species_energy_file=Path("species_energies.csv")
        )

    # Initiate reaction energy calculator
    calculator = ReactionEnergyCalculator(
        external_potential=external_potential,
        pH=pH,
        verbose=True,
        )

    # Calculate energy changes
    energy_changes = calculator.calculate_energy_change(reaction_pathways, energy_reader)

    # Print energy changes
    calculator.print_energy_changes(energy_changes)

    # Generate reaction diagram plot
    plotter = DiagramPlotter(energy_changes)
    plotter.generate_plot()

def parse_command_line_arguments():
    """
    Parse command line arguments for external potential and pH values.

    Returns:
        float: External potential value.
        float: pH value.
    """
    parser = argparse.ArgumentParser(description='Description of your program')
    parser.add_argument('-U', '--external_potential', type=float, default=0, help='External potential in volts')
    parser.add_argument('-ph', '--pH', type=float, default=7, help='pH value (0 to 14)')
    args = parser.parse_args()

    return args.external_potential, args.pH

if __name__ == "__main__":
    main()
