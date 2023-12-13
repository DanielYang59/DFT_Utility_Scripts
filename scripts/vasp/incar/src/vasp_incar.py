#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pathlib import Path
import warnings
from typing import Dict

class VaspIncar:
    """
    Class for handling VASP INCAR files.
    """
    def __init__(self, file: Path) -> None:
        """
        Initialize a VaspIncar instance.

        Parameters:
        - file (Path): The path to the INCAR file.

        Raises:
        - AssertionError: If the provided file is not a valid file.

        The __init__ method imports and checks the INCAR file, raising an
        AssertionError if the file is not a valid file. It then reads the INCAR
        data using the _read_in method and checks the INCAR entries using the
        _check_incar method.
        """
        # Import and check INCAR file
        assert file.is_file()
        self.file = file
        self.incar_data = self._read_in()
        self._check_incar()


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


    def _read_in(self) -> Dict[str, str]:
        """
        Read the INCAR file, skipping empty lines and comments (# or !).

        Inline comments at the end of lines are also skipped.
        """
        incar_data = {}

        with open(self.file, 'r') as f:
            for line in f:
                # Remove inline comments (comments at the end of the line)
                line = line.split('#')[0].split('!')[0].strip()

                if not line:
                    continue  # Skip empty and comment lines

                if self._check_incar(line):
                    tag, value = map(str.strip, line.split("="))
                    incar_data[tag] = value

        return incar_data


    def read_tag(self, name: str, default: str = None) -> str:
        """
        Read the value associated with the specified tag from the INCAR data.

        Parameters:
        - name (str): The tag name.
        - default (str): The default value to return if the tag is not found.

        Returns:
        - str: The value associated with the tag, or the default value if not found.
        """
        return self.incar_data.get(name, default)


    def set_tag(self, name: str, value: str) -> None:
        """
        Set the value associated with the specified tag in the INCAR data.

        If the tag is already present, update its value. Otherwise, add a new key-value pair.

        Parameters:
        - name (str): The tag name.
        - value (str): The value to associate with the tag.
        """
        self.incar_data[name] = value


    def write_out(self, new_file: Path) -> None:
        """
        Write the INCAR data to a new file.

        Parameters:
        - new_file (Path): The path to the new INCAR file.
        """
        with open(new_file, 'w') as f:
            for tag, value in self.incar_data.items():
                f.write(f"{tag} = {value}\n")
