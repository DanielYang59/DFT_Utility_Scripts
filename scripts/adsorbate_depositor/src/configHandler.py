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
        Check config.yaml tags.
        """

        # Check distance
        distance = config_data.get('distance', None)
        if not isinstance(distance, (int, float)) or distance < 0:
            raise ValueError("Invalid distance value. It should be a non-negative float/int.")
        elif distance <= 1:
            warnings.warn(f"Distance in config.yaml set to {distance}, might be too small?")

        # Check auto_reposition
        auto_reposition = config_data.get('auto_reposition', None)
        if not isinstance(auto_reposition, bool):
            raise ValueError("Invalid auto_reposition value. It should be a boolean.")

        # Check adsorbate_source and adsorbate_path
        adsorbate_source = config_data.get('adsorbate_source', None)
        adsorbate_path = config_data.get('adsorbate_path', None)
        if adsorbate_source not in ["POSCAR", "DATABASE"]:
            raise ValueError("Invalid adsorbate_source. It should be either 'POSCAR' or 'DATABASE'.")
        elif adsorbate_source == "POSCAR":
            if not Path(adsorbate_path).is_file():
                raise FileNotFoundError("Invalid adsorbate_path. Should point to a file when adsorbate_source is 'POSCAR'.")
        else:
            if not Path(adsorbate_path).is_dir():
                raise FileNotFoundError("Invalid adsorbate_path. Should point to a directory when adsorbate_source is 'DATABASE'.")

        # Check sites
        sites = config_data.get('sites', None)
        if not isinstance(sites, dict):
            raise TypeError("Invalid sites entry. Should be a dictionary.")
        for key, value in sites.items():
            site_keys = [int(k) for k in key.split('_') if k.isdigit()]
            if len(site_keys) == 1 and value != "top":
                raise ValueError(f"Invalid value for site key {key}. Should be 'top' for single-site.")
            elif len(site_keys) == 2 and value != "bridge":
                raise ValueError(f"Invalid value for site key {key}. Should be 'bridge' for two-site.")
            elif len(site_keys) >= 3 and value not in ["centre", "center"]:
                raise ValueError(f"Invalid value for site key {key}. Should be 'centre' or 'center' for three or more sites.")

    def load_config(self):
        """
        Load and check the existing config.yaml file.
        """
        with open(self.config_path, "r") as f:
            config_data = yaml.safe_load(f)
        self._check_config()
        return config_data

    def copy_config(self, template_path):
        """
        Copy a template config.yaml file to the current working directory.
        """
        shutil.copy(template_path, self.working_dir)
        print(f"Copied template config.yaml to {self.working_dir}")
        exit()
