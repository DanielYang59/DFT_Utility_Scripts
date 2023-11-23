#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pathlib import Path
import numpy as np

class OutputPdosGenerator:
    def __init__(self, pdos_data: np.ndarray, energies: np.ndarray) -> None:
        """TODO:"""

        # Check source data type
        if not isinstance(pdos_data, np.ndarray):
            raise TypeError("Expect PDOS data in numpy arrays.")
        if not isinstance(energies, np.ndarray):
            raise TypeError("Expect energy data in numpy arrays.")

        # Check source data shapes
        if pdos_data.ndim != 2:
            raise ValueError("Expect PDOS data in (, NEDOS) shape.")
        if energies.ndim != 1:
            raise ValueError("Expect 1D energy data.")
        if pdos_data.shape[1] != energies.shape[0]:
            raise ValueError("PDOS data and energy data shape mismatch.")

        # Update attributes
        self.pdos_data = pdos_data
        self.energies = energies

    def write(self, filename: Path) -> None:
        pass
        # Add header to the source data


        # Output data as csv file

