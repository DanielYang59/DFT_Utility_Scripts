#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pathlib import Path
import yaml
import shutil

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

    def load_config(self):
        """
        Load the existing config.yaml file.
        """
        with open(self.config_path, "r") as f:
            config_data = yaml.safe_load(f)
        return config_data

    def copy_config(self, template_path):
        """
        Copy a template config.yaml file to the current working directory.
        """
        shutil.copy(template_path, self.working_dir)
        print(f"Copied template config.yaml to {self.working_dir}")
        exit()
