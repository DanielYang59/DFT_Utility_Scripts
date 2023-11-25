#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from pathlib import Path


class UserConfigParser:
    def __init__(self, configfile: Path) -> None:
        # Check config file
        if configfile.is_fife():
            self.configfile = configfile

        else:
            raise FileNotFoundError(f"PDOS extractor config file {configfile} not found.")

    def generate_config_template(self):
        pass

    def _parse_curve_info(self, curve_info: str) -> list:
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

    def _parse_atom_selection(self, atom_selections: str) -> list:
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
        return atom_selections_by_index

    def read_config(self):
        pass

# Test area
if __name__ == "__main__":
    pass
