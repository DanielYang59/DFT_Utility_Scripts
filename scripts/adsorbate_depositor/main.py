#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pathlib import Path

from src.configHandler import ConfigHandler
from src.adsorbateGenerator import AdsorbateGenerator
from src.siteGenerator import SiteGenerator
from src.adsorbateDepositor import AdsorbateDepositor

def main():
    # Read config.yaml or copy the template
    cfg_handler = ConfigHandler()

    if cfg_handler.check_config_exists():
        config = cfg_handler.load_config()
    else:
        cfg_handler.copy_config_template(template_path=Path("database") / "config_template.yaml")

    # Generate sites
    site_generator = SiteGenerator(
        POSCAR_substrate=config["substrate"]["path"],
        distance=config["deposit"]["distance"],
        sites=config["substrate"]["sites"]
        )
    sites = site_generator.generate()

    # Generate adsorbates and adsorbate reference points
    adsorbate_generator = AdsorbateGenerator(
        work_mode=config["adsorbate"]["source"],
        generate_rotations=config["adsorbate"]["rotation"],
        )

    adsorbates = adsorbate_generator.generate_adsorbates(
        path=config["adsorbate"]["path"],
        atom_indexes=config["adsorbate"]["atom_indexes"],
        pathway_name=config["adsorbate"]["pathway_name"],
        )

    adsorbate_refs = adsorbate_generator.generate_adsorbate_references(
        adsorbates,

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
        target_vacuum_level=config["deposit"]["target_vacuum_level"],
        center_along_z=config["deposit"]["center_along_z"],
        fix_substrate=config["deposit"]["fix_substrate"],
        )

    # Write generate model to file
    structure_generator.write()

if __name__ == "__main__":
    main()
