#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pathlib import Path
import warnings

class VaspIncar:
    """
    Class for handling VASP INCAR files.
    """
    def __init__(self, file: Path) -> None:
        assert file.is_file()
        self.file = file
        self.incar_data = {}

    def _check_incar(self) -> bool:
        """
        Check if there are empty values in the INCAR data.

        Returns:
        - bool: True if all values are non-empty, False otherwise.
        """
        for tag, value in self.incar_data.items():
            if not value:
                warnings.warn(f"Empty value found for tag '{tag}' in INCAR. Please check the input.")
                return False
        return True

    def read(self) -> None:
        """
        Read the INCAR file, skipping empty lines and comments (# or !).

        Inline comments at the end of lines are also skipped.
        """
        with open(self.file, 'r') as f:
            for line in f:
                # Remove inline comments (comments at the end of the line)
                line = line.split('#')[0].split('!')[0].strip()

                if not line:
                    continue  # Skip empty and comment lines

                if self._check_incar(line):
                    tag, value = map(str.strip, line.split("="))
                    self.incar_data[tag] = value

        self._check_incar()

    def write(self, new_file: Path) -> None:
        """
        Write the INCAR data to a new file.

        Parameters:
        - new_file (Path): The path to the new INCAR file.
        """
        with open(new_file, 'w') as f:
            for tag, value in self.incar_data.items():
                f.write(f"{tag} = {value}\n")
