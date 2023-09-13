#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pathlib import Path
import pandas as pd
import json

def read_molecular_species_csv(filepath: Path) -> pd.DataFrame:
    """
    Reads molecular species energy data from a CSV file.

    Parameters:
        filepath (Path): The path to the CSV file.

    Returns:
        pd.DataFrame: A DataFrame containing the molecular species data.
    """
    # Use pandas to read the CSV file into a DataFrame
    df = pd.read_csv(filepath)

    # Check for required columns
    required_columns = ["Name", "Energy"]
    for col in required_columns:
        if col not in df.columns:
            raise ValueError(f"Missing required column: {col}")

    return df

def read_intermediate_csv(filepath: Path) -> pd.DataFrame:
    """
    Reads intermediate species energy data (including ZPE and entropy corrections) from a CSV file.

    Parameters:
        filepath (Path): The path to the CSV file.

    Returns:
        pd.DataFrame: A DataFrame containing the intermediate species data.
    """
    # Use pandas to read the CSV file into a DataFrame
    df = pd.read_csv(filepath)

    # Check for required columns
    required_columns = ["Name", "Energy", "ZPE", "Entropy"]
    for col in required_columns:
        if col not in df.columns:
            raise ValueError(f"Missing required column: {col}")

    return df

def read_reaction_pathway(json_path: str) -> dict:
    """
    Read the reaction pathway from a JSON file.

    Parameters:
        json_path (str): The path to the JSON file containing the reaction pathway.

    Returns:
        dict: A dictionary representing the reaction pathway.
    """
    json_path = Path(json_path)

    if not json_path.exists():
        raise FileNotFoundError(f"The specified JSON file {json_path} does not exist.")

    with json_path.open("r") as f:
        data = json.load(f)

    # Check tags
    required_tags = ["Reaction_Name", "External_Conditions", "Intrinsic_Properties"]
    for tag in required_tags:
        if tag not in data:
            raise ValueError(f"Required tag {tag} not found in JSON file.")

    external_conditions = ["pH", "applied_potential_V", "target_temperature_K"]
    for condition in external_conditions:
        if condition not in data["External_Conditions"]:
            raise ValueError(f"Required condition {condition} not found in JSON file.")

        value = data["External_Conditions"][condition]
        if not isinstance(value, (float, int)):
            raise TypeError(f"{condition} should be a float or integer.")

    intrinsic_properties = ["equilibrium_potential_V", "Reaction_Steps"]
    for prop in intrinsic_properties:
        if prop not in data["Intrinsic_Properties"]:
            raise ValueError(f"Required intrinsic property {prop} not found in JSON file.")

        if prop == "equilibrium_potential_V":
            value = data["Intrinsic_Properties"][prop]
            if not isinstance(value, (float, int)):
                raise TypeError(f"{prop} should be a float or integer.")

    return data
