#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pathlib import Path
import csv

def write_output_pdos(pdos_data: list, fermi_level: float, filename: Path) -> None:
    """
    Write PDOS data to a CSV file.

    Parameters:
    - pdos_data (list): List containing tuples (energy_array, pdos_spin_up, pdos_spin_down) for each curve.
    - fermi_level (float): Fermi level used for reference.
    - filename (Path): Path to the output CSV file.

    Raises:
    - FileExistsError: If the output file already exists.

    """
    # Write header
    header = ["Curve", "Energy", "PDOS_Spin_Up", "PDOS_Spin_Down"]

    # Write data for each curve, one column at a time
    with open(filename, mode='w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(header)

        # Iterate through each energy level for all curves before moving to the next column
        for energy_level in zip(*[curve[0] for curve in pdos_data]):
            for index, curve in enumerate(pdos_data):
                # Unpack (energy_array, pdos_spin_up, pdos_spin_down) tuple
                energy_array, pdos_spin_up, pdos_spin_down = curve

                # Reference energy to fermi level
                energy_level_ref = energy_level[index] - fermi_level

                # Write data for the current energy level
                csv_writer.writerow([f"Curve_{index + 1}", energy_level_ref, pdos_spin_up[index], pdos_spin_down[index]])

