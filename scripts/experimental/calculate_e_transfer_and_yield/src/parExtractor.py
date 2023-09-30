#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pathlib import Path
import pandas as pd
import re
from typing import List, Dict

class ParExtractor:
    """
    Extracts data section from a .par file and provides methods to manipulate the data.

    Parameters:
        par_file (Path): The path to the .par file to be processed.

    Raises:
        FileNotFoundError: If the provided file is not found or does not have a '.par' extension.

    Methods:
        extract_columns(datasection_name: str, columns: List[str]) -> Dict[str, pd.Series]:
            Extracts specified columns from the data section and returns them as a dictionary of Pandas Series.

    """
    def __init__(self, par_file: Path) -> None:
        """
        Initializes the ParExtractor object with the provided .par file path.

        Args:
            par_file (Path): Path to the .par file.

        Raises:
            FileNotFoundError: If the provided file is not found or does not have a '.par' extension.

        """
        # Validate input .par file
        if par_file.is_file() and par_file.name.endswith(".par"):
            self.par_file = par_file

        else:
            raise FileNotFoundError("Invalid .par file provided.")

    def _load_and_extract_section(self, skip_lines: int = 2) -> str:
        """
        Extracts content between specified section headers in the .par file.

        Args:
            skip_lines (int): Number of lines to skip in the data section (default is 2).

        Raises:
            RuntimeError: If the specified data section is not found in the file.

        """
        # Define data section name
        start_tag = f"<{self.datasection_name}>"
        end_tag = f"</{self.datasection_name}>"
        pattern = re.compile(f"{re.escape(start_tag)}(.*?)\\n{re.escape(end_tag)}", re.DOTALL)

        # Import and extract data section to str
        with open(self.par_file, 'r') as file:
            content = file.read()
            match = pattern.search(content)
            if match:
                extracted_data = match.group(1).strip()
                if skip_lines is None:
                    self.section_data = extracted_data.split("\n")
                else:
                    self.section_data = extracted_data.split("\n")[skip_lines:]

            else:
                raise RuntimeError(f"Segment '{self.datasection_name}' not found in the file.")

    def _section_to_dataframe(self) -> pd.DataFrame:
        """
        Converts the extracted data section to a Pandas DataFrame.

        Raises:
            ValueError: If the number of columns in the header does not match the number of data columns.

        Returns:
            pd.DataFrame: Extracted data section as a DataFrame.

        """
        headers = [i.strip() for i in self.section_data[0].strip().split(",")[:-1]]
        data = [line.strip().split(",") for line in self.section_data[1:]]

        if len(headers) != len(data[0]):
            raise ValueError(f"Number of columns in header ({len(headers)}) does not match data ({len(data[0])}).")

        return pd.DataFrame(data, columns=headers)

    def extract_columns(self, datasection_name: str, columns: List(str)) -> Dict[str, pd.DataFrame]:
        """
        Extracts specified columns from the data section and returns them as a dictionary of Pandas Series.

        Args:
            datasection_name (str): Name of the data section in the .par file.
            columns (List[str]): Names of the columns to extract.

        Returns:
            Dict[str, pd.Series]: Dictionary containing extracted columns as Pandas Series.

        Raises:
            KeyError: If any specified column is not found in the data section.
        """
        # Load .par file and extract datasection
        self.datasection_name = datasection_name
        self._load_and_extract_section()

        # Convert extracted datasection to Pandas DataFrame
        df = self._section_to_dataframe()

        # Extract selected columns into a dictionary
        extracted_columns = {}
        for column_name in columns:
            if column_name in df.columns:
                extracted_columns[column_name] = df[column_name]
            else:
                raise KeyError(f"Column '{column_name}' not found in the DataFrame.")

        return extracted_columns
