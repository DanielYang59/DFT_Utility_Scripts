#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import yaml
from pathlib import Path

class ReadmeAssembler:
    """A class to generate a README.md file based on a YAML 'recipe' file.

    This class provides a way to dynamically generate a README.md file by
    concatenating individual markdown sections specified in a YAML recipe file.
    The recipe file defines the order and source files for each section to be
    included in the final README.md.

    Attributes:
        recipe (list): A list of dictionaries, each containing information about
                       a section to be included in the README.md.

    Methods:
        __init__(recipe_file: Path): Initialize ReadmeGenerator with a recipe file.
        _parse_recipe(recipe_file_path: Path): Parse the YAML recipe file.
        generate(output_file: Path, overwrite: bool = True): Generate the README file.
    """

    def __init__(self, recipe_file: Path) -> None:
        """Initialize ReadmeGenerator with a recipe file.

        Args:
            recipe_file (Path): Path to the YAML recipe file.

        Raises:
            FileNotFoundError: Raised if the file does not exist.
        """
        # Load README recipe file
        self.recipe_file_path = recipe_file.resolve()
        self.recipe = self._parse_recipe(recipe_file)

    def _parse_recipe(self, recipe_file_path: Path) -> dict:
        """
        Parse a YAML file containing the 'recipe' for the README.

        Parameters:
            recipe_file_path (Path): The path to the YAML file.

        Returns:
            list: A list of dictionaries, each containing information about a section of the README.
        """
        try:
            with recipe_file_path.open("r", encoding="utf-8") as file:
                recipe_data = yaml.safe_load(file)
                return recipe_data.get("readme_sections", [])

        except FileNotFoundError:
            print(f"File {recipe_file_path} not found.")
            return []

        except yaml.YAMLError as exc:
            print(f"Error in YAML file: {exc}")
            return []

    def generate(self, output_file: Path, overwrite: bool = True):
        """Generate the README file.

        Args:
            output_file (Path): Path to the README.md file to generate.
            overwrite (bool, optional): Whether to overwrite the file if it exists. Defaults to True.
        """
        if output_file.is_file() and not overwrite:
            raise FileExistsError("Target README file already exists and overwrite is disabled.")

        # Concatenate section files to form README
        readme_content = ""
        for section in self.recipe:
            # Make the path relative to the location of the recipe file
            section_path = self.recipe_file_path.parent / section["source"]
            if section_path.is_file():
                with section_path.open("r", encoding="utf-8") as file:
                    readme_content += file.read() + "\n\n"

        # Write README to file
        with output_file.open("w", encoding="utf-8") as file:
            file.write(readme_content)

def main():
    recipe_file = Path(".maintenance/generate_readme/readme_recipe.yaml")
    output_file = Path("./README.md")
    generator = ReadmeAssembler(recipe_file)
    generator.generate(output_file)

if __name__ == "__main__":
    main()
