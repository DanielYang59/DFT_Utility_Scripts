#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pathlib import Path
import yaml
import shutil
import warnings

class ConfigHandler:
    """
    Class to handle operations related to the config.yaml file.
    """

    def __init__(self):
        """
        Initialize ConfigHandler and find the location of config.yaml.
        """
        self.working_dir = Path.cwd()
        self.config_path = self.working_dir / "config.yaml"

    def check_config_exists(self):
        """
        Check if config.yaml exists in the current working directory.
        """
        if self.config_path.exists():
            return True
        else:
            print(f"config.yaml does not exist at {self.config_path}")
            return False

    def _check_config(self, config_data):
        """
        Check updated config.yaml tags.
        """

        # Check substrate
        substrate = config_data.get('substrate', {})
        sites = substrate.get('sites', [])
        for site in sites:
            site_keys = [int(k) for k in site.split('_') if k.isdigit()]
            if len(site_keys) < 1:
                raise ValueError(f"Invalid value for site key {site}. Should contain at least one integer.")

        # Check adsorbate
        adsorbate = config_data.get('adsorbate', {})
        source = adsorbate.get('source', None)
        path = adsorbate.get('path', None)
        rotation = adsorbate.get('rotation', None)

        if source not in ["POSCAR", "DATABASE"]:
            raise ValueError("Invalid adsorbate source. It should be either 'POSCAR' or 'DATABASE'.")

        if source == "POSCAR" and not Path(path).is_file():
            raise FileNotFoundError("Invalid path. Should point to a file when source is 'POSCAR'.")
        elif source == "DATABASE" and not Path(path).is_dir():
            raise FileNotFoundError("Invalid path. Should point to a directory when source is 'DATABASE'.")

        if not isinstance(rotation, bool):
            raise ValueError("Invalid rotation value. It should be a boolean.")

        # Check deposit
        deposit = config_data.get('deposit', {})
        distance = deposit.get('distance', None)
        auto_reposition = deposit.get('auto_reposition', None)

        if not isinstance(distance, (int, float)) or distance < 0:
            raise ValueError("Invalid distance value. It should be a non-negative float/int.")

        if not isinstance(auto_reposition, bool):
            raise ValueError("Invalid auto_reposition value. It should be a boolean.")

    def load_config(self):
        """
        Load and check the existing config.yaml file.
        """
        with open(self.config_path, "r") as f:
            config_data = yaml.safe_load(f)
        self._check_config(config_data)
        return config_data

    def copy_config(self, template_path):
        """
        Copy a template config.yaml file to the current working directory.
        """
        shutil.copy(template_path, self.working_dir)
        print(f"Copied template config.yaml to {self.working_dir}")
        exit()
