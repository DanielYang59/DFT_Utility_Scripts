#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
from typing import List, Tuple
from pathlib import Path

def write_pdos_to_file(pdos_data: List[Tuple], fermi_level: float, output_file: Path):
    """
    Write pDOS data to a CSV file.

    Parameters:
        pdos_data (List[Tuple]): List of tuples, each containing PDOS data for a curve.
                              Tuple format: (energy_array, spin_up_dos, spin_down_dos)
                              spin_down_dos is None if ISPIN = 1.
        fermi_level (float): Fermi level energy used to reference the energy_array.
        output_file (Path): Path to the output CSV file.

    Raises:
        ValueError: If the input list of pdos_data is empty.

    The function processes each tuple in pdos_data, where each tuple represents a curve with PDOS data.
    It creates a DataFrame with columns for curve separator, energy, spin_up_dos, and spin_down_dos (if applicable).
    The curve separator is generated as 'curve_index' followed by the index of the curve in pdos_data.
    The energy values are referenced to the provided fermi_level.
    The resulting DataFrame is saved to the specified output_file in CSV format.
    """
    # Check if the pdos_data list is not empty
    if not pdos_data:
        raise ValueError("The input list of pdos_data is empty.")

    # Create an empty DataFrame to store the results
    result_df = pd.DataFrame()

    # Loop through each requested curve
    for index, data in enumerate(pdos_data):
        # Unpack each "data" tuple of (energy_array, spin_up_dos, spin_down_dos)
        energy_array, spin_up_dos, spin_down_dos = data

        # Reference energy to fermi level
        energy_array -= fermi_level

        # Generate curve separator column
        curve_separator = np.full(len(energy_array), f"curve_{index + 1}")

        # Create a DataFrame for the current curve
        curve_df = pd.DataFrame({
            'curve_separator': curve_separator,
            'energy_fermi': energy_array,
            'spin_up_dos': spin_up_dos,
            'spin_down_dos': spin_down_dos if spin_down_dos is not None else np.nan
        })

        # Concatenate the current curve DataFrame to the result DataFrame
        result_df = pd.concat([result_df, curve_df], axis=1)

    # Save the result DataFrame to the specified output file
    result_df.to_csv(output_file, index=False)
