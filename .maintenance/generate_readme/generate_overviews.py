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


def generate_overviews():
    # Initialize the generator
    generator = OverviewsGenerator(Path("./scripts"))

    # Read the project structure file


    # Extract README parts from each dir to assemble a master overview


if __name__ == "__main__":
    generate_overviews()
