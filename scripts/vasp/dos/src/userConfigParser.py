#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pathlib import Path
from typing import List
from shutil import copyfile

class UserConfigParser:
    def __init__(self, configfile: Path) -> None:
        # Check config file
        self.configfile = configfile

    def generate_config_template(self, config_template_file: Path) -> None:
        """
        Copy the provided configuration template file to the current working directory.

        Parameters:
            config_template_file (Path): The path to the configuration template file.

        Raises:
            FileNotFoundError: If the specified `config_template_file` does not exist.
        """

        # Check if the file exists before copying
        if not config_template_file.exists():
            raise FileNotFoundError(f"Error: Config template file '{config_template_file}' not found.")

        else:
            # Get the filename from the path
            filename = config_template_file.name

            # Set the destination path to the current working directory
            destination_path = Path.cwd() / filename

            # Copy the file to the destination path
            copyfile(config_template_file, destination_path)

            print(f"Config template file '{filename}' copied to '{destination_path}'")

    def _check_and_parse_curve_info(self, curve_info: str) -> list:
        """
        Parses the curve information string and confirm the orbital selections to binary values.

        Parameters:
            curve_info (str): The curve information string containing orbital selections.

        Returns:
            list: A list containing the standardized curve information with binary orbital selections.
        """
        # Check curve info string
        if not isinstance(curve_info, str) or len(curve_info.split()) != 17:
            raise TypeError(f"Please check curve info line: {curve_info}.")

        curve_info = curve_info.split()

        # Standardize curve selection entry to binary integers
        standardized_curve_info = [curve_info[0], ]
        for selection in curve_info[1:]:
            if selection not in {"0", "1"}:
                raise ValueError(f"Illegal orbital selection {selection}.")

            standardized_curve_info.append(int(selection))

        return standardized_curve_info

    def _parse_atom_selection(self, atom_selections: str) -> List[int]:
        """
        Parse atom selections.
        # NOTE: Indexing starts from 1 for single selections and element matches.

        Allowed atom selections:
        1. By index, for example: "1" (starting from 1)
        2. By index range, for example: "1-5"
        3. By element type, for example: "Fe"
        4. Mix of 1-3 separated by "_"
        5. "all" for all atoms

        Parameters:
            atom_selections (str): String representing atom selections.

        Returns:
            list: List of selected atom indices (starting from 1).
        """
        # Parse atom selections
        if atom_selections == "all":
            return list(range(1, len(self.atom_list) + 1))

        atom_selections_by_index = []
        for selection in atom_selections.split("_"):
            # Single atom selection: "1"
            if selection.isdigit():
                atom_selections_by_index.append(int(selection))

            # Range selection: "1-3"
            elif "-" in selection:
                start, end = map(int, selection.split('-'))
                atom_selections_by_index.extend(list(range(start, end + 1)))

            # Element selection: "Fe"
            else:
                atom_selections_by_index.extend([(index + 1) for index, value in enumerate(self.atom_list) if value == selection])

        assert len(atom_selections_by_index) == len(set(atom_selections_by_index)), "Duplicate atom selections detected."
        if not atom_selections_by_index:
            raise ValueError(f"No match found for atom request: {atom_selections}.")
        return atom_selections_by_index

    def read_config(self, atom_list: List[int]) -> list:
        """
        Reads and processes a configuration file, updating the atom list and parsing curve information.

        Parameters:
            atom_list (List[int]): A list of atom indices.

        Returns:
            List[list]: A list of processed lines from the configuration file, where each line is a list representing the parsed information. The first element of each line is updated using the _parse_atom_selection method.
        """
        # Take atom list
        self.atom_list = atom_list

        # Fetch each line in config file
        with self.configfile.open(mode="r") as file:
            lines = file.readlines()

        # Filter out comments and empty lines
        lines = [line.strip() for line in lines if not line.strip().startswith('#') and line.strip()]

        # Post-process each curve
        processed_lines = []
        for line in lines:
            line = self._check_and_parse_curve_info(line)

            # Parse atom selection
            line[0] = self._parse_atom_selection(line[0])

            processed_lines.append(line)

        return processed_lines
