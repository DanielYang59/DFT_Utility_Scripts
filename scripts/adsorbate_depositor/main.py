#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pathlib import Path

from src.configHandler import ConfigHandler
from src.adsorbateGenerator import AdsorbateGenerator
from src.siteGenerator import SiteGenerator
from src.structureGenerator import StructureGenerator

def main():
    # Read config.yaml or copy the template
    cfg_handler = ConfigHandler()

    if cfg_handler.check_config_exists():
        config = cfg_handler.load_config()
    else:
        cfg_handler.copy_config(template_path=Path("database") / "config_template.yaml")

    # Generate sites
    site_generator = SiteGenerator()
    sites = site_generator.generate_sites()

    # Generate adsorbates
    adsorbate_generator = AdsorbateGenerator()
    adsorbates = adsorbate_generator.generate_adsorbates()

    # Generate adsorbate-on-site structure files
    structure_generator = StructureGenerator(
        distance=config["distance"],
        auto_reposition=config["auto_reposition"]
        )
    for site in sites:
        for ads in adsorbates:
            structure_generator.deposit(substrate_POSCAR, site, ads)

if __name__ == "__main__":
    pass
