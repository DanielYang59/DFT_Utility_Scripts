#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pathlib import Path
import yaml
import shutil

class YAMLConfigParser:
    def __init__(self, config_file_path: Path, template_file_path: Path) -> None:
        # Check if config file exists
        if config_file_path.is_file():
            self.config_file_path = Path(config_file_path)

        else:
            self.copy_template(template_file_path)

    def load_yaml(self) -> dict:
        """
        Load YAML data from the config file.

        Returns:
            dict: Parsed YAML data.
        """
        with open(self.config_file_path, 'r') as file:
            data = yaml.safe_load(file)
        return data

    def copy_template(self, template_file_path: Path) -> None:
        """
        Copy template file if config file doesn't exist in current working dir.

        Args:
            template_file_path (Path): Path to the template config.yaml file

        """
        # Check if template config file exists
        if not template_file_path.is_file():
            raise FileNotFoundError(f"Template config file {template_file_path} not found.")

        shutil.copy(template_file_path, Path.cwd())
        raise FileNotFoundError("Config file not found in current working dir. A template would be copied.")
