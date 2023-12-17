#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# TODO: need to fix final subdir extraction
# TODO: include links to children README.md


import os
from pathlib import Path
import re
import json
from typing import List, Union
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
        """Generate a list of paths pointing to each final subdirectory under the 'scripts' directory.

        Returns:
            List[Path]: A list of paths pointing to each final subdirectory.
        """
        def generate_paths_from_structure(structure: dict, current_path: Union[Path, str] = "") -> List[Path]:
            """Generate paths from a project structure.

            Args:
                structure (dict): The project structure dictionary.
                current_path (Union[Path, str]): The current path during traversal.

            Returns:
                List[Path]: A list of paths pointing to each final subdirectory.
            """
            paths = []
            for key, value in structure.items():
                sub_path = Path(current_path) / key
                if not value:
                    paths.append(sub_path)

                else:
                    paths.extend(generate_paths_from_structure(value, sub_path))
            return paths


        return generate_paths_from_structure(self.project_structure, "scripts")


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


        # Temporary fix of dirs (remove the first two elements)
        # DEBUG # TODO:
        self.final_dirs = [Path(*path.parts[2:]) for path in self.final_dirs]


    def _search_readmes(self) -> List[Path]:
        """Search for README.md files based on the project structure.

        Returns:
            List[Path]: A list of paths to README.md files found in the specified directories.

        Raises:
            Warning: If README.md is not found in a directory specified by the project structure.
        """
        readmes = []

        # Search for README.md files based on the structure json file
        for dir_path in self.final_dirs:
            readme_path = dir_path /'README.md'
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
                # Insert headers
                header = "/".join(str(file).split(os.sep)[:-1])
                # TODO: would need a better solution than this
                return f"## {header}\n{overview_match.group(1).strip()}\n"

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
