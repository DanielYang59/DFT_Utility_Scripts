#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import matplotlib as mpl
from typing import Dict, List, Optional
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

    def _calculate_absolute_energies(self, energies: List[float]):
        """
        Calculate absolute energies based on the delta energy changes.
        
        Args:
            input_list (List[float]): List of floats representing delta values.

        Returns:
            List[float]: List of absolute values calculated based on deltas.
        """
        abs_energies = [0]  # Starting with 0 as the initial value
        current_value = 0  # Initialize the current value
        
        for delta in energies:
            current_value += delta
            abs_energies.append(current_value)

        assert len(abs_energies) == len(energies) + 1
        return abs_energies
        
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
        mpl.rcParams['axes.linewidth'] = 2.5

        fig, ax = plt.subplots(figsize=(10, 6))

        # Sort the energy changes dictionary based on reaction steps
        sorted_steps = sorted(self.energy_changes.keys())
        energies = [self.energy_changes[step] for step in sorted_steps]
        
        # Recalculate absolute energy positions
        energies = self._calculate_absolute_energies(energies)

        # Create a horizontal line for each energy with a length of 0.75 units at the center of every reaction step
        for i in range(len(sorted_steps)):
            step = sorted_steps[i]
            energy = energies[i]
            line_center = step  # the center of the step
            ax.hlines(y=energy, xmin=line_center - 0.375, xmax=line_center + 0.375, color='black', linewidth=4)

            # Add a dotted line connecting the end of this line with the start of the next line
            if i < len(sorted_steps) - 1:
                next_step = sorted_steps[i + 1]
                next_energy = energies[i + 1]
                next_line_center = next_step  # the center of the next step
                ax.plot([line_center + 0.375, next_line_center - 0.375], [energy, next_energy], color='black', linestyle='dotted', linewidth=2.5)

        # Set x-ticks and y-ticks to display reaction steps and energy values
        plt.xticks(range(len(sorted_steps) + 1), [str(i) for i in range(len(sorted_steps) + 1)], fontsize=20)
        plt.yticks(fontsize=20)

        # Set labels
        plt.xlabel('Reaction Step', fontsize=20)
        plt.ylabel('Free Energy Change (eV)', fontsize=20)

        # Set x-axis to start from 0
        plt.xlim(0, len(sorted_steps) + 1)

        # Set tick length to 5
        ax.tick_params(axis='both', length=5, width=2.5)

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
