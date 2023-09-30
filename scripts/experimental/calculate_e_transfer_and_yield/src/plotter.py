#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import numpy as np
from typing import Dict, List

class e_transfer_and_yield_plotter:
    def __init__(self, data: Dict[str, List[np.ndarray]], config: Dict[str, list], savename: str = "figure.png") -> None:
        """
        Initializes the e_transfer_and_yield_plotter object.

        Args:
            data (Dict[str, List[np.ndarray]]): A dictionary where keys are sample names
                                                and values are lists of numpy arrays representing data.
                                                The first array is x values, the second is H2O2 yield,
                                                and the third is electron transfer numbers.
            config (Dict[str, list]): A dictionary containing configuration data.
                                      (Not used in the current implementation.)

        Raises:
            TypeError: If data is not a dictionary or if the inner lists do not contain numpy arrays.
        """
        if not isinstance(data, dict):
            raise TypeError("data must be a dictionary.")

        for sample_data in data.values():
            if not (isinstance(sample_data, list) and len(sample_data) == 3 and
                    all(isinstance(arr, np.ndarray) for arr in sample_data)):
                raise TypeError("Each value in data dictionary must be a list containing three numpy arrays.")

        self.savename = savename

    def plot(self):
        """
        Plots H2O2 yield and electron transfer numbers for each sample in the data dictionary.

        """
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 6), sharex=True)

        for sample_name, sample_data in self.data.items():
            x = sample_data[0]
            h2o2_yield = sample_data[1]
            electron_transfer_numbers = sample_data[2]

            ax1.plot(x, h2o2_yield, label=f'{sample_name} - H2O2 yield')
            ax2.plot(x, electron_transfer_numbers, label=f'{sample_name} - Electron transfer numbers')

        ax1.set_ylabel('H2O2 Yield')
        ax2.set_ylabel('Electron Transfer Numbers')
        ax2.set_xlabel('X Label')  # You can replace 'X Label' with your actual x-axis label

        ax1.legend()
        ax2.legend()

        plt.tight_layout()
        plt.savefig(self.savename, dpi=600)
        plt.show()
