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

    # Write each curve to file
    with open(filename, mode='w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)

        for index, curve in enumerate(pdos_data):
            # Unpack (energy_array, pdos_spin_up, pdos_spin_down) tuple
            energy_array, pdos_spin_up, pdos_spin_down = curve

            # Reference energy to fermi level
            energy_array -= fermi_level

            # Write separator column (curve_index)
            separator_column = [f"Curve {index}"] * len(energy_array)
            csv_writer.writerow(separator_column)

            # Write energy_array, pdos_spin_up, pdos_spin_down to the CSV file
            header = ["Energy", "PDOS_Spin_Up"]
            if pdos_spin_down is not None:
                header.append("PDOS_Spin_Down")

            csv_writer.writerow(header)

            rows = zip(energy_array, pdos_spin_up, pdos_spin_down) if pdos_spin_down is not None else zip(energy_array, pdos_spin_up)
            csv_writer.writerows(rows)
