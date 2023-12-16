#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import json
from pathlib import Path
from asciitree import LeftAligned

class ProjectStructureGenerator:
    def __init__(self, structure_recipe: Path) -> None:
        """
        Initialize the ProjectStructureGenerator.

        Parameters:
        - structure_recipe (Path): The path to the JSON file containing the project structure recipe.

        Raises:
        - AssertionError: If the specified structure recipe file does not exist.

        Loads the project structure recipe from the specified JSON file and stores it in the
        `structure_data` attribute for later use in generating the project structure tree.
        """
        # Load structure recipe file
        if structure_recipe.is_file():
            with open(structure_recipe, 'r') as file:
                self.structure_data = json.load(file)
        else:
            raise FileNotFoundError("Project structure recipe file not found.")


    def generate_structure_tree(self) -> str:
        """
        Generate a tree structure string from the project structure data.

        Returns:
        - str: The formatted tree structure string.

        Notes:
            reference: https://github.com/mbr/asciitree
        """
        return LeftAligned()(self.structure_data)


    def create_readme_part(self, structure_tree: str, filename: Path) -> None:
        """
        Create a README part file with the project structure.

        Parameters:
        - structure_tree (str): The tree structure string to be written to the file.
        - filename (Path): The path to the README part file.

        Writes the project structure to the specified Markdown file.
        The generated file will include a title and the formatted project structure.

        """
        # Write project structure to .md file
        with open(filename, 'w') as file:
            file.write("# Project Structure\n")
            file.write(structure_tree)


def generate_project_structure():
    # Initialize the generator and read recipe file
    generator = ProjectStructureGenerator(structure_recipe=Path("./project_structure_recipe.json"))

    # Generate structure tree string
    structure_tree = generator.generate_structure_tree()

    # Create README part file
    generator.create_readme_part(structure_tree, filename=Path("./readme_parts/project_structure.md"))

if __name__ == "__main__":
    generate_project_structure()
