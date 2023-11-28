# PDOS Extractor

PDOS extractor is a Python tool designed for extracting and processing partial density of states (pDOS) information from VASP calculations.

## Overview

This tool simplifies the extraction of pDOS data from VASP's vasprun.xml files.

## Usage

To use the PDOS Extractor, follow these steps:

1. **Run the extraction script:**

   - Execute the `extract_pdos.py` script using the following command:
     ```bash
     python3 extract_pdos.py
     ```
2. **Configure PDOS parameters:**

   - After running the script, a template configuration file named `PDOSIN.template` will be generated. Open this file in a text editor of your choice.
   - Modify the entries and rename it to `PDOSIN`. This includes specifying the atom selections, and orbital selections.
   - Save the changes to the `PDOSIN` file.
3. **Rerun the extraction script:**

   - Once you have configured the parameters in the `PDOSIN` file, rerun the `extract_pdos.py` script to generate the pDOS data based on your custom settings:
     ```bash
     python3 extract_pdos.py
     ```
4. **Review the results:**

   - The script will generate output files containing the extracted pDOS information. You can analyze these files to obtain insights into the partial density of states for your VASP calculations.
