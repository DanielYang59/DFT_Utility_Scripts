#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from pathlib import Path

class ReactionPathwayParser:
    def __init__(self, file: Path) -> None:
        # Check reaction pathway file
        if not file.is_file() or file.suffix != ".json":
            raise FileNotFoundError(f"Reaction pathway json file '{file}' not found or illegal.")
        self.file = file

        # Import and parse reaction pathway yaml file
        self.data = self._import_pathway_file()

        # Check reaction pathway
        self._check_pathway()

    def _import_pathway_file(self) -> dict:
         # Load and parse the JSON file
        with open(self.file, 'r') as json_file:
            try:
                data = json.load(json_file)
                return data
            except json.JSONDecodeError as exc:
                print(f"Error parsing JSON file '{self.file}': {exc}")

    def _check_pathway(self):
        pass

    def calculate_free_energy_change(self):
        pass
