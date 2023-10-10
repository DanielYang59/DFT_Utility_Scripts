#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
from typing import Dict, Optional
from pathlib import Path

class DiagramPlotter:
    def __init__(self, energy_changes: Dict[int, float]) -> None:
        """
        Initialize the DiagramPlotter with energy_changes dictionary.

        Args:
            energy_changes (dict): Dictionary where keys are integers (reaction steps) and
                values are floats (corresponding energy changes).
        """
        self.energy_changes = energy_changes

    def generate_plot(self, saveplot: Optional[bool] = False, path: Optional[Path] = None, show_plot: Optional[bool] = True) -> None:
        """
        Generate and optionally save/display a reaction diagram plot based on energy_changes.

        Args:
            saveplot (bool, optional): Whether to save the plot. Defaults to False.
            path (Path, optional): The path where the plot will be saved. Defaults to None.
            show_plot (bool, optional): Whether to display the plot. Defaults to True.

        Returns:
            None
        """
        fig, ax = plt.subplots(figsize=(10, 6))

        # Sort the energy changes dictionary based on reaction steps
        sorted_steps = sorted(self.energy_changes.keys())
        energies = [self.energy_changes[step] for step in sorted_steps]

        # Create a horizontal line for each energy at every reaction step
        for idx, (step, energy) in enumerate(zip(sorted_steps, energies)):
            ax.hlines(y=energy, xmin=0, xmax=step, color='black', linewidth=2)

        # Set x-ticks and y-ticks to display reaction steps and energy values
        plt.xticks(range(1, len(sorted_steps) + 1), sorted_steps, fontsize=20)
        plt.yticks(fontsize=20)

        # Set labels
        plt.xlabel('Reaction Step', fontsize=20)
        plt.ylabel('Free Energy Change (eV)', fontsize=20)

        # Set savefig DPI to 300
        plt.rcParams['savefig.dpi'] = 300

        # Save the plot if saveplot is True
        if saveplot:
            if path is None:
                path = Path.cwd() / 'reaction_diagram.png'
            plt.savefig(path, bbox_inches='tight')

        # Display the plot if show_plot is True
        if show_plot:
            plt.show()

# Test area
if __name__ == "__main__":
    # Generate test data
    test_data = {
        1: 2.5, 2: -3.0, 3: 4.0, 4: -5.5,
        5: 6.0, 6: -1.5, 7: 0.5, 8: -2.0
    }

    # Initiate diagram plotter
    plotter = DiagramPlotter(test_data)

    # Generate and show diagram plot
    plotter.generate_plot()
