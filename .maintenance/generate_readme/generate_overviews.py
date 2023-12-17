#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# TODO: include link to children README.md


from pathlib import Path
import re
import json


class OverviewsGenerator:
    """This class is responsible for generating the Overviews part of the README.md.

    """

    def __init__(self, root_dir: Path) -> None:
        """Initialize the OverviewsGenerator with the root directory.

        Args:
            root_dir (str): The root directory where to start generating the Overviews.
        """
        if not root_dir.is_dir():
            raise FileNotFoundError(f"Working dir {root_dir} not found.")
        self.root_dir = Path(root_dir)
        self.overviews = []

    def read_structure_file(self, filename: Path) -> None:
        """Read the project structure file.

        Args:
            filename (Path): The path to the project structure JSON file.
        """
        with open(filename, 'r', encoding='utf-8') as json_file:
            self.project_structure = json.load(json_file)

    def read_readmes(self, directory):
        """Read README.md file and extract the overview.

        Args:
            directory (Path): The directory to read README.md from.

        Returns:
            str: Extracted overview or None if not found.
        """
        readme_path = directory / 'README.md'
        if readme_path.exists():
            with open(readme_path, 'r', encoding='utf-8') as readme_file:
                readme_content = readme_file.read()
                overview_match = re.search(r'<!--\s*overview\s*:\s*(.*?)\s*-->', readme_content, re.DOTALL | re.IGNORECASE)
                if overview_match:
                    return overview_match.group(1).strip()
        return None

    def process_directory(self, directory):
        """Process a directory, read README, and extract overview.

        Args:
            directory (Path): The directory to process.
        """
        overview = self.read_readmes(directory)
        if overview:
            self.overviews.append(overview)

        subdirectories = self.project_structure.get(str(directory.relative_to(self.root_dir)), {})
        for subdirectory in subdirectories:
            self.process_directory(directory / subdirectory)

    def extract_and_cat_overviews(self) -> str:
        """Extract and concatenate overviews from directories.

        Returns:
            str: Concatenated overview.
        """
        self.process_directory(self.root_dir)
        return '\n\n'.join(self.overviews)


def generate_overviews():
    # Initialize the generator
    generator = OverviewsGenerator(Path("."))  # script should be executed right under root dir

    # Read the project structure file
    generator.read_structure_file(Path(".maintenance/generate_readme/project_structure_recipe.json"))

    # Extract README parts from each dir to assemble a master overview
    master_overview = generator.extract_and_cat_overviews()

    print(master_overview)  # DEBUG

    # Write master overview to the README file
    with open(".maintenance/generate_readme/readme_parts/overviews.md", 'w', encoding='utf-8') as readme_file:
        readme_file.write("\n\n<!-- overview: master -->\n")
        readme_file.write(master_overview)


if __name__ == "__main__":
    generate_overviews()
