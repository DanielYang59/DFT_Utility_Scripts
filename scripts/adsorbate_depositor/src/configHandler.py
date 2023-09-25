#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# TODO: avoid overwrite existing template (if not config.yaml in cwd but already a config_template.yaml)

from pathlib import Path
import yaml
import shutil

class ConfigHandler:
    """
    Class to handle operations related to the config.yaml file.
    """

    def __init__(self, config_filename="config.yaml", template_filename="config_template.yaml"):
        """
        Initialize ConfigHandler and find the location of the configuration file.

        Parameters:
            config_filename (str): The name of the configuration file. Default is 'config.yaml'.
            template_filename (str): The name of the template file. Default is 'config_template.yaml'.
        """
        self.config_dir = Path(config_filename).parent
        self.config_path = Path(config_filename)
        self.template_path = Path(template_filename)

    def _convert_relative_paths(self, config_data):
        """
        Convert relative paths to absolute paths based on the directory of config.yaml.

        Parameters:
            config_data (dict): The configuration data.
        """
        config_data['substrate']['path'] = str(self.config_dir / Path(config_data['substrate']['path']))
        config_data['adsorbate']['path'] = str(self.config_dir / Path(config_data['adsorbate']['path']))
        config_data['deposit']['output_dir'] = str(self.config_dir / Path(config_data['deposit']['output_dir']))

    def check_config_exists(self):
        """
        Check if the configuration file exists in the current working directory.

        Returns:
            bool: True if the configuration file exists, otherwise False.
        """
        if self.config_path.exists():
            return True
        else:
            print(f"{self.config_path.name} does not exist at {self.config_path}")
            return False

    def check_template_exists(self):
        """
        Check if the template file exists in the current working directory to avoid overwriting.

        Returns:
            bool: True if the template file exists, otherwise False.
        """
        if self.template_path.exists():
            print(f"{self.template_path.name} already exists in {self.working_dir}. Avoiding overwrite.")
            return True
        return False

    def _check_config(self, config_data):
        """
        Check config.yaml tags.
        """

        # Check "substrate" tags
        substrate = config_data.get('substrate', {})
        sites = substrate.get('sites', [])
        for site in sites:
            site_keys = [int(k) for k in site.split('_') if k.isdigit()]
            if len(site_keys) < 1:
                raise ValueError(f"Invalid value for site key {site}. Should contain at least one integer.")

        # Check "adsorbate" tags
        adsorbate = config_data.get('adsorbate', {})
        source = adsorbate.get('source', None)
        path = adsorbate.get('path', None)
        rotation = adsorbate.get('rotation', None)
        atom_indexes = adsorbate.get('atom_indexes', [])
        reference = adsorbate.get('reference', [])

        if source not in ["POSCAR", "DATABASE"]:
            raise ValueError("Invalid adsorbate source. It should be either 'POSCAR' or 'DATABASE'.")

        if source == "POSCAR" and not Path(path).is_file():
            raise FileNotFoundError("Invalid path. Should point to a file when source is 'POSCAR'.")
        elif source == "DATABASE" and not Path(path).is_dir():
            raise FileNotFoundError("Invalid path. Should point to a directory when source is 'DATABASE'.")

        if not isinstance(rotation, bool):
            raise ValueError("Invalid rotation value. It should be a boolean.")

        # Check POSCAR mode tags
        if source == "POSCAR":
            if not all(isinstance(index, int) and index >= 1 for index in atom_indexes):
                raise ValueError(f"Invalid atom_indexes {atom_indexes}. Should be a list of integers >= 1.")

            if len(set(atom_indexes)) != len(atom_indexes):
                raise ValueError("Duplicate atom indexes are not allowed.")

            if not all(isinstance(index, int) and index >= 1 for index in reference):
                raise ValueError("Invalid reference. Should be a list of integers >= 1.")

            if len(set(reference)) != len(reference):
                raise ValueError("Duplicate reference indexes are not allowed.")

        # Check "deposit" tags
        deposit = config_data.get('deposit', {})
        distance = deposit.get('distance', None)
        auto_offset_along_z = deposit.get('auto_offset_along_z', None)

        if not isinstance(distance, (int, float)) or distance < 0:
            raise ValueError("Invalid distance value. It should be a non-negative float/int.")

        if not isinstance(auto_offset_along_z, bool):
            raise ValueError("Invalid auto_offset_along_z value. It should be a boolean.")

    def load_config(self) -> dict:
        """
        Load and validate the existing configuration file.

        Returns:
            dict: The validated configuration data.
        """
        with open(self.config_path, "r") as f:
            config_data = yaml.safe_load(f)
        self._check_config(config_data)
        self._convert_relative_paths(config_data)  # Convert relative paths to absolute
        return config_data

    def copy_config_template(self, template_path):
        """
        Copy a template configuration file to the current working directory.

        Parameters:
            template_path (str): The path to the template file.
        """
        if not self.check_template_exists():
            shutil.copy(template_path, self.working_dir)
            print(f"Copied template {self.template_path.name} to {self.working_dir}")
        else:
            raise FileExistsError("Template config file found in current dir. Template generation aborted.")
