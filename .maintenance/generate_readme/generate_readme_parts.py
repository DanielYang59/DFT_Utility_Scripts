#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pathlib import Path
import re

class ReadmePartsGenerator:
    """This class is responsible for generating dynamic parts of the README.md file.

    It generates a tree-like directory structure and extracts 'Overview' sections
    from README files within each directory.
    """

    def __init__(self, root_dir: Path) -> None:
        """Initialize the ReadmePartsGenerator with the root directory.

        Args:
            root_dir (str): The root directory where to start generating the README parts.
        """
        # Check working dir
        if not root_dir.is_dir():
            raise FileNotFoundError(f"Working dir {root_dir} not found.")
        self.root_dir = Path(root_dir)

    def save_to_file(self, content: str, file_path: Path) -> None:
        """Save content to a specified file.

        Args:
            content (str): The content to save.
            file_path (Path): The path to the file where to save the content.
        """
        with file_path.open("w") as f:
            f.write(content)

    def generate_tree_structure(self, exclude: list = None) -> str:
        """Generate a string that represents the tree-like directory structure.

        Args:
            exclude (list): List of directory or filenames to exclude.

        Returns:
            str: The string representation of the directory structure.
        """
        if exclude is None:
            exclude = []

        def _generate_tree(dir_path, prefix=""):
            entries = []
            for entry in dir_path.iterdir():
                if entry.name not in exclude:
                    if entry.is_dir():
                        entries.append(f"{prefix}├── {entry.name}/")
                        entries.extend(_generate_tree(entry, prefix + "│   "))
                    # Uncomment below if you want to include files as well
                    # else:
                    #     entries.append(f"{prefix}├── {entry.name}")
            return entries

        tree_str = '\n'.join(_generate_tree(self.root_dir))
        return tree_str

    def _extract_overview(self, readme_path: Path) -> str:
        """Extract the 'Overview' section from a given README.md file.

        Args:
            readme_path (Path): Path to the README.md file.

        Returns:
            str: Extracted 'Overview' section as a string.
        """
        # Import README
        if not readme_path.is_file():
            raise FileNotFoundError(f"README {readme_path} not found.")
        with readme_path.open("r") as f:
            text = f.read()

        # Get the "Overview" part
        overview_match = re.search(r"## Overview\n(.+?)(##|$)", text, re.DOTALL)
        return overview_match.group(1).strip() if overview_match else f"Overview not found in {readme_path}."

    def generate_overviews(self) -> str:
        """Generate Markdown-formatted overviews by reading READMEs from directories.

        Returns:
            str: Markdown-formatted text containing overviews.
        """
        overviews = []
        for dir_entry in self.root_dir.iterdir():
            if dir_entry.is_dir():
                readme_path = dir_entry / "README.md"
                if readme_path.exists():
                    overview = self._extract_overview(readme_path)
                    overviews.append(f"### {dir_entry.name}\n{overview}\n")

        return "\n".join(overviews)

def main():
    # Initialize README generator
    readme_gen = ReadmePartsGenerator(Path("../../scripts"))

    # Generate tree structure
    tree_structure = readme_gen.generate_tree_structure(exclude=[".git", "__pycache__"])
    readme_gen.save_to_file(tree_structure, Path("readme_parts/project_structure.md"))

    # Generate overviews
    overviews = readme_gen.generate_overviews()
    readme_gen.save_to_file(overviews, Path("readme_parts/overviews.md"))

if __name__ == "__main__":
    main()
