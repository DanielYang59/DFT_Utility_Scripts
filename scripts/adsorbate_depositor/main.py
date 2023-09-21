#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pathlib import Path
from src.configHandler import ConfigHandler
from src.adsorbateGenerator import AdsorbateGenerator
from src.siteGenerator import SiteGenerator
from src.adsorbateDepositor import AdsorbateDepositor

def load_configuration():
    """Load or create configuration.

    Returns:
        dict: Loaded configuration or None if a template was copied.
    """
    cfg_handler = ConfigHandler()
    if cfg_handler.check_config_exists():
        return cfg_handler.load_config()
    else:
        cfg_handler.copy_config_template(template_path=Path("database") / "config_template.yaml")
        return None

def main():
    """Main entry point for the project."""
    config = load_configuration()
    if config is None:
        print("No configuration loaded. Exiting.")
        return

    # Generate sites
    sites = SiteGenerator(
        POSCAR_substrate=config["substrate"]["path"],
        distance=config["deposit"]["distance"],
        sites=config["substrate"]["sites"]
    ).generate()

    # Generate adsorbates and adsorbate reference points
    adsorbate_generator = AdsorbateGenerator(
        work_mode=config["adsorbate"]["source"],
        path=config["adsorbate"]["path"],
        pathway_name=config["adsorbate"]["pathway_name"],
        generate_rotations=config["adsorbate"]["rotation"],
    )

    adsorbates = adsorbate_generator.generate_adsorbates(atom_indexes=config["adsorbate"]["atom_indexes"])

    adsorbate_refs = adsorbate_generator.generate_adsorbate_references(
        adsorbates_dict=adsorbates,
        poscar_ads_ref=config["adsorbate"]["None"]
    )

    # Generate adsorbate-on-site structure files
    structure_generator = AdsorbateDepositor(
        POSCAR_substrate=config["substrate"]["path"],
        sites=sites,
        adsorbates=adsorbates,
        adsorbate_refs=adsorbate_refs,
    )

    structure_generator.deposit(
        auto_offset_along_z=config["deposit"]["auto_offset_along_z"],
        fix_substrate=config["deposit"]["fix_substrate"],
        # target_vacuum_level=config["deposit"]["target_vacuum_level"],
        # center_along_z=config["deposit"]["center_along_z"],
    )

    # Write generated model to file
    structure_generator.write(output_dir=config["deposit"]["output_dir"])

if __name__ == "__main__":
    main()
