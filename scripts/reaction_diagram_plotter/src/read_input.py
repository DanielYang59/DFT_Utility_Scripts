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

def read_reaction_data(json_path: str) -> dict:
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

    with json_path.open("r", encoding="utf-8") as f:
        data = json.load(f)

    # Checking keys in "Reaction_Steps"
    reaction_steps = data["Intrinsic_Properties"]["Reaction_Steps"]
    step_keys = [int(key) for key in reaction_steps.keys() if key.isdigit()]

    if len(step_keys) != len(reaction_steps):
        raise ValueError("All keys in Reaction_Steps should be integers.")

    step_keys.sort()

    for i, key in enumerate(step_keys):
        if key != i + 1:
            raise ValueError("Step integers should be continuous and greater than 0.")

    return data
