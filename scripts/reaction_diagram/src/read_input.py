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

    return data
