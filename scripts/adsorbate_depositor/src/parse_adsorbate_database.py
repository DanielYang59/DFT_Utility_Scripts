#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pathlib import Path
import yaml
import re

def parse_adsorbate_database(path: Path, pathway_name: str, header: str = "pathway_database_header.yaml") -> dict:
    """
    Parses and validates a YAML file containing database information about adsorbate reaction pathways and steps.

    Args:
        path (Path): The path to the directory containing the YAML file.
        pathway_name (str): The name of the specific pathway to return.
        header (str): The name of the YAML header file. Default is "pathway_database_header.yaml".

    Returns:
        dict: A dictionary representation of the adsorbates within the selected pathway. None if pathway_name doesn't exist.
    """

    header_path = path / header

    if not header_path.is_file():
        raise FileNotFoundError(f"The header YAML file {header_path} does not exist.")

    with header_path.open("r") as f:
        database_dict = yaml.safe_load(f)

    # Validate the loaded dictionary
    pathways = database_dict.get('pathways', {})

    if not pathways:
        raise ValueError("No pathways found in the database.")

    for i, (pathway_key, steps) in enumerate(pathways.items(), start=1):
        if f"pathway_{i}" != pathway_key:
            raise ValueError(f"Pathway keys must be indexed continuously from 1. Found {pathway_key} instead.")

        step_names = set()
        step_count = 0  # Reset step_count for each pathway

        for j, (step_key, step_data) in enumerate(steps.items(), start=1):
            if re.match(r'step_\d+', step_key):  # Checks if key matches "step_N" pattern
                step_count += 1
                if f"step_{step_count}" != step_key:
                    raise ValueError(f"Step keys in {pathway_key} must be indexed continuously from 1. Found {step_key} instead.")

                name = step_data.get("name")
                if not name:
                    raise ValueError(f"Missing 'name' for {step_key} in {pathway_key}.")

                if name in step_names:
                    raise ValueError(f"Duplicate name {name} found in {pathway_key}.")
                step_names.add(name)

                adsorbate_atoms = step_data.get("adsorbate_atoms")
                reference_atoms = step_data.get("reference_atoms")

                if not adsorbate_atoms or not reference_atoms:
                    raise ValueError(f"Empty 'adsorbate_atoms' or 'reference_atoms' in {step_key} of {pathway_key}.")

                if not set(reference_atoms).issubset(set(adsorbate_atoms)):
                    raise ValueError(f"'reference_atoms' must be a subset of 'adsorbate_atoms' in {step_key} of {pathway_key}.")

                if len(adsorbate_atoms) != len(set(adsorbate_atoms)) or len(reference_atoms) != len(set(reference_atoms)):
                    raise ValueError(f"Duplicate atoms found in 'adsorbate_atoms' or 'reference_atoms' in {step_key} of {pathway_key}.")

                if any(isinstance(x, int) and x < 0 for x in adsorbate_atoms) or any(isinstance(x, int) and x < 0 for x in reference_atoms):
                    raise ValueError(f"Negative integers found in 'adsorbate_atoms' or 'reference_atoms' in {step_key} of {pathway_key}.")

    pathway_dict = pathways.get(pathway_name, None)
    if pathway_dict is None:
        raise ValueError(f"Pathway {pathway_name} does not exist in the database.")

    return pathway_dict
