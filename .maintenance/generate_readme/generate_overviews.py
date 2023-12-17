#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# TODO: include links to children README.md


from pathlib import Path
import re
import json
from typing import List
import warnings


class OverviewsGenerator:
    """This class is responsible for generating the Overviews part of the README.md.

    """

    def __init__(self, root_dir: Path) -> None:
        """Initialize the OverviewsGenerator with the root directory.

        Args:
            root_dir (str): The root directory where to start generating the Overviews.
        """
        if not root_dir.is_dir():
            raise FileNotFoundError(f"Root dir {root_dir} not found.")
        self.root_dir = Path(root_dir)


    def _generate_final_subdirs(self) -> List[Path]:
        # TODO:
        final_subdirs = []
        pass


    def read_structure_file(self, filename: Path) -> None:
        """Read the project structure json file and genetate paths to final subdirectories.

        Args:
            filename (Path): The path to the project structure JSON file.
        """
        # Load project structure json file
        with open(filename, 'r', encoding='utf-8') as json_file:
            self.project_structure = json.load(json_file)


        # Get final subdirectories to extract README.md
        self.final_dirs = self._generate_final_subdirs()


    def _search_readmes(self) -> List[Path]:
        """Search for README.md files based on the project structure.

        Returns:
            List[Path]: A list of paths to README.md files found in the specified directories.

        Raises:
            Warning: If README.md is not found in a directory specified by the project structure.
        """
        readmes = []

        # Search for README.md files based on the structure json file
        for dir_path in self.project_structure:
            readme_path = self.root_dir / dir_path /'README.md'
            if readme_path.exists():
                readmes.append(readme_path)

            else:
                warnings.warn(f"README.md not found in {dir_path}.")

        return readmes


    def _extract_overview(self, file: Path) -> str:
        """Extract the 'Overview' section from the specified README.md file.

        Args:
            file (Path): The path to the README.md file.

        Returns:
            str: Extracted overview or an empty string if not found.
        """
        with open(file, 'r', encoding='utf-8') as readme_file:
            readme_content = readme_file.read()
            overview_match = re.search(r'## Overview\n\n(.+?)\n\n', readme_content, re.DOTALL)
            if overview_match:
                return overview_match.group(1).strip()
        return ''


    def extract_and_concat_overviews(self) -> str:
        """Extract and concatenate overviews from README.md under given directories.

        Returns:
            str: Concatenated overview.
        """
        # Search directories in structure file for README.md Paths
        readmes = self._search_readmes()


        # Extract the "Overview" section from the README.md file
        overviews = [self._extract_overview(f) for f in readmes]


        # Concatenate README parts
        return '\n'.join(overviews)


def generate_overviews():
    # Initialize the generator
    generator = OverviewsGenerator(Path("."))  # script should be executed right under root dir


    # Read the project structure file
    generator.read_structure_file(Path(".maintenance/generate_readme/project_structure_recipe.json"))


    # Extract README parts from each dir to assemble a master overview
    master_overview = generator.extract_and_concat_overviews()


    # Write master overview to the README file
    with open(Path(".maintenance/generate_readme/readme_parts/overviews.md"), 'w', encoding='utf-8') as readme_file:
        readme_file.write("\n\n# Project Overviews\n")
        readme_file.write(master_overview)


if __name__ == "__main__":
    generate_overviews()
