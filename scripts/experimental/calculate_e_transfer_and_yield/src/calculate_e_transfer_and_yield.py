#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pathlib import Path
import numpy as np

from .parExtractor import ParExtractor

class Calculator:

    def __init__(self, sample_name: str, disk_suffix: str, ring_suffix: str, constant_N: float) -> None:
        """
        Initialize the Calculator object.

        Args:
            sample_name (str): The name of the sample.
            disk_suffix (str): The suffix for disk data .par file.
            ring_suffix (str): The suffix for ring data .par file.
            constant_N (float): Constant N value used in the calculations.

        Raises:
            TypeError: If constant_N is not a valid float.

        """
        # Compile file names
        self.sample_name = sample_name
        self.disk_suffix = disk_suffix
        self.ring_suffix = ring_suffix

        # Validate constant N in formula
        if not isinstance(constant_N, (float, int)):
            raise TypeError("Invalid datatype for constant N.")
        self.constant_N = constant_N

        # Prepare data for electron transfer number and H2O2 yield calculation
        self._prepare_data()

    def _prepare_data(self) -> None:
        """
        Load and prepare data from disk and ring data .par files.
        Converts data to NumPy arrays and stores them as class attributes.

        """
        # Load disk data
        disk_extractor = ParExtractor(par_file=Path.cwd() / f"{self.sample_name}{self.disk_suffix}.par")
        disk_data_dict = disk_extractor.extract_columns(datasection_name="Segment1", columns=["E(V)", "I(A)"])

        # Extract disk data
        self.Ed = np.array(disk_data_dict["E(V)"], dtype=float)
        self.Id = np.array(disk_data_dict["I(A)"], dtype=float)

        # Load ring data
        ring_extractor = ParExtractor(par_file=Path.cwd() / f"{self.sample_name}{self.ring_suffix}.par")
        ring_data_dict = ring_extractor.extract_columns(datasection_name="Segment1", columns=["E(V)", "I(A)"])

        # Extract ring data
        self.Er = np.array(ring_data_dict["E(V)"], dtype=float)
        self.Ir = np.array(ring_data_dict["I(A)"], dtype=float)

    def extract_potential(self, source: str = "disk", offset: float = 0.0) -> np.ndarray:
        """
        Extract potential values for either disk or ring data with an optional offset.

        Args:
            source (str, optional): Potential source ("disk" or "ring"). Defaults to "disk".
            offset (float, optional): Potential offset value. Defaults to 0.0.

        Returns:
            np.ndarray: Extracted potential values.

        Raises:
            ValueError: If an invalid potential source is provided.

        """
        # Check potential source
        if source == "disk":
            return np.copy(self.Ed) + offset

        elif source == "ring":
            return np.copy(self.Er) + offset

        else:
            raise ValueError(f"Invalid potential source selection {source}.")

    def calculate_e_transfer(self) -> np.ndarray:
        """
        Calculate electron transfer number using the provided data.

        Returns:
            np.ndarray: Array of calculated electron transfer numbers.

        """
        return 4 * (abs(self.Id) / (abs(self.Id) + self.Ir / self.constant_N))

    def calculate_yield(self) -> np.ndarray:
        """
        Calculate H2O2 yield in percentage using the provided data.

        Returns:
            np.ndarray: Array of calculated H2O2 yields in percentage.

        """
        return 200 * ((self.Ir / self.constant_N) / (abs(self.Id) + self.Ir / self.constant_N))
