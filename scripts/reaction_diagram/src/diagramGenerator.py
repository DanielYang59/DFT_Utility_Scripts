#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
from pathlib import Path

class ReactionDiagramGenerator:
    def __init__(self, deltaG_dict: dict, store_path: Path = Path("output")/"reaction_diagram.png"):
        self.deltaG_dict = deltaG_dict
        self.store_path = store_path
        self.prev_endpoint = None

    def _configure_plot(self):
        plt.figure(figsize=(10, 5))
        for axis in ['top', 'bottom', 'left', 'right']:
            plt.gca().spines[axis].set_linewidth(2)
        plt.locator_params(axis='y', nbins=5)
        plt.tick_params(axis="both", which="major", length=5, width=2.5, labelsize=12)

    def _draw_horizontal_lines(self, linewidth=3):
        for i, (step, energy) in enumerate(self.deltaG_dict.items()):
            plt.hlines(y=energy, xmin=i + 1 - 1/6, xmax=i + 1 + 1/6, colors='k', linewidth=linewidth)

    def _draw_dotted_lines(self, linewidth=2):
        self.prev_endpoint = None  # Resetting to None before drawing dotted lines
        for i, (step, energy) in enumerate(self.deltaG_dict.items()):
            current_endpoint = (i + 1 + 1/6, energy)
            if self.prev_endpoint is not None:
                plt.plot([self.prev_endpoint[0], current_endpoint[0] - 1/3], [self.prev_endpoint[1], energy], 'k--', linewidth=linewidth)
            self.prev_endpoint = current_endpoint

    def _save_plot(self):
        self.store_path.parent.mkdir(parents=True, exist_ok=True)
        plt.tight_layout()
        plt.savefig(self.store_path, dpi=300)
        plt.show()

    def generate(self):
        self._configure_plot()
        self._draw_horizontal_lines()
        self._draw_dotted_lines()
        self._save_plot()

# Test area
if __name__ == "__main__":
    test_deltaG_dict = {
        "step_1": -0.2,
        "step_2": 0.1,
        "step_3": -0.3,
        "step_4": 0.05,
        "step_5": 0.2,
        "step_6": -0.1,
        "step_7": 0.15,
        "step_8": -0.05,
    }

    diagram_generator = ReactionDiagramGenerator(test_deltaG_dict)
    diagram_generator.generate()
