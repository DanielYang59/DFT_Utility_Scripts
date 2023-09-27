#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# TODO: fix project structure
# TODO: create link to child READMEs

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
        if not root_dir.is_dir():
            raise FileNotFoundError(f"Working dir {root_dir} not found.")
        self.root_dir = Path(root_dir)

    def save_to_file(self, content: str, file_path: Path, header: str = "", wrap_code_block: bool = False) -> None:
        """Save content to a specified file.

        Args:
            content (str): The content to save.
            file_path (Path): The path to the file where to save the content.
            header (str): The header to prepend to the content.
            wrap_code_block (bool): Whether to wrap the content in a Markdown code block.
        """
        with file_path.open("w") as f:
            if header:
                f.write(f"{header}\n\n")
            if wrap_code_block:
                f.write("```\n")
            f.write(content)
            if wrap_code_block:
                f.write("\n```\n")

    @staticmethod
    def _generate_tree(dir_path: Path, prefix="", exclude=None) -> list:
        """Internal static method to generate the directory tree structure.

        Args:
            dir_path (Path): The directory path to generate the tree for.
            prefix (str): The prefix for the current recursion.
            exclude (list): List of directory names to exclude.

        Returns:
            list: A list of strings representing the directory tree.
        """
        lines = []
        child_dirs = [child for child in dir_path.iterdir() if child.is_dir() and child.name not in exclude]

        should_include_children = any((child / "README.md").exists() for child in child_dirs)

        for child in sorted(child_dirs):
            child_lines = ReadmePartsGenerator._generate_tree(child, prefix + "    ", exclude)
            if child_lines:
                lines.extend([f"{prefix}│   {line}" for line in child_lines])

        if (dir_path / "README.md").exists() or should_include_children:
            lines.append(f"{prefix}└── {dir_path.name}")

        return lines

    def generate_tree_structure(self, exclude: list = None) -> str:
        """Generate a string that represents the tree-like directory structure.

        Args:
            exclude (list): List of directory or filenames to exclude.

        Returns:
            str: The string representation of the directory structure.
        """
        if exclude is None:
            exclude = []

        tree_str = '\n'.join(reversed(self._generate_tree(self.root_dir, exclude=exclude)))
        return tree_str

    def _extract_overview(self, readme_path: Path) -> str:
        """Extract the 'Overview' section from a given README.md file.

        Args:
            readme_path (Path): Path to the README.md file.

        Returns:
            str: Extracted 'Overview' section as a string.
        """
        if not readme_path.is_file():
            raise FileNotFoundError(f"README {readme_path} not found.")
        with readme_path.open("r") as f:
            text = f.read()

        overview_match = re.search(r"## Overview\n(.+?)(##|$)", text, re.DOTALL)
        return overview_match.group(1).strip() if overview_match else f"Overview not found in {readme_path}."

    def generate_overviews(self) -> str:
        """Generate Markdown-formatted overviews by reading READMEs from directories.

        Returns:
            str: Markdown-formatted text containing overviews.
        """
        overviews = []

        # Recursively find all directories containing a README.md file
        for dir_entry in self.root_dir.rglob('*'):
            if dir_entry.is_dir():
                readme_path = dir_entry / "README.md"
                if readme_path.exists():
                    # Include the parent directory
                    parent_dir = dir_entry.relative_to(self.root_dir)
                    overview = self._extract_overview(readme_path)
                    overviews.append(f"## {parent_dir}\n{overview}\n")

        if not overviews:
            raise AssertionError("No overviews were found.")

        return "\n".join(overviews)

def main():
    # Initialize README generator
    readme_gen = ReadmePartsGenerator(Path("./scripts"))

    # Generate tree structure
    tree_structure = readme_gen.generate_tree_structure(exclude=[".git", "__pycache__"])
    readme_gen.save_to_file(tree_structure, Path(".maintenance/generate_readme/readme_parts/project_structure.md"), header="# Project Structure", wrap_code_block=True)

    # Generate overviews
    overviews = readme_gen.generate_overviews()
    readme_gen.save_to_file(overviews, Path(".maintenance/generate_readme/readme_parts/overviews.md"), header="# Module Overviews", wrap_code_block=False)

if __name__ == "__main__":
    main()
