#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# TODO: include link to child READMEs

from pathlib import Path
import re

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

    def _extract_overview(self, readme_path: Path) -> str:
        """Extract the 'Overview' section from a given README.md file.

        Args:
            readme_path (Path): Path to the README.md file.

        Returns:
            str: Extracted 'Overview' section as a string.
        """
        if not readme_path.is_file():
            raise FileNotFoundError(f"README {readme_path} not found.")
        with readme_path.open("r", encoding="utf-8") as f:
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
    # Initialize the generator
    generator = OverviewsGenerator(Path("./scripts"))

    # Generate the Overviews
    overviews = generator.generate_overviews()
    # TODO:


if __name__ == "__main__":
    main()
