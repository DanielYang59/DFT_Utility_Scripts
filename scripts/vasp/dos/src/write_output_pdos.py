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
    # Check output file name
    if filename.is_file():
        raise FileExistsError(f"Error: File '{filename}' already exists. Exiting to avoid overwriting.")

    # Write each curve's header to file
    with open(filename, mode='w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)

        header = ["Curve", "Energy", "PDOS_Spin_Up", "PDOS_Spin_Down"]
        csv_writer.writerow(header)

        # Write data for each curve
        for index, curve in enumerate(pdos_data):
            # Unpack (energy_array, pdos_spin_up, pdos_spin_down) tuple
            energy_array, pdos_spin_up, pdos_spin_down = curve

            # Reference energy to fermi level
            energy_array -= fermi_level

            # Write data for each energy level
            for energy, spin_up, spin_down in zip(energy_array, pdos_spin_up, pdos_spin_down):
                csv_writer.writerow([f"Curve_{index + 1}", energy, spin_up, spin_down])
