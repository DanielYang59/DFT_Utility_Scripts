#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import json
from pathlib import Path
from asciitree import LeftAligned
from collections import OrderedDict as OD

class ProjectStructureGenerator:
    def __init__(self, structure_recipe: Path) -> None:
        # Load structure recipe file
        assert structure_recipe.is_file()
        with open(self.structure_recipe, 'r') as file:
            self.structure_data = json.load(file)

    def generate_structure_tree(self) -> str:
        pass


    def create_readme_part(self, structure_tree: str, filename: Path) -> None:

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
