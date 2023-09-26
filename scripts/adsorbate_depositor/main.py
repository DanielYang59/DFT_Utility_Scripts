#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# TODO: fix script running path and file read path (relative to running path)

import sys
from pathlib import Path

root_dir = str(Path(__file__).resolve().parents[1])
sys.path.append(root_dir)

from src.configHandler import ConfigHandler
from src.adsorbateGenerator import AdsorbateGenerator
from src.siteGenerator import SiteGenerator
from src.adsorbateDepositor import AdsorbateDepositor

def main():
    """
    Main entry point for the computational material science project. This function orchestrates the workflow for generating,
    placing, and saving atomistic structures with adsorbates on substrate surfaces.

    Workflow:
    1. Checks for the existence of a configuration file and loads it if found. If not found, a template is copied.
    2. Generates adsorption sites on the substrate surface using the SiteGenerator class.
    3. Generates various adsorbate structures using the AdsorbateGenerator class.
    4. Deposits the adsorbates onto the substrate surface at the generated sites using the AdsorbateDepositor class.
    5. Writes the generated structures to output files.

    Configuration file:
    The program relies on a YAML-based configuration file for various settings. The ConfigHandler class is responsible for
    managing this configuration.

    Output:
    Atomistic structures of substrate with adsorbates are saved in the specified output directory.

    """
    # Load or generate the configuration
    cfg_handler = ConfigHandler(Path.cwd() / "config.yaml")
    if cfg_handler.check_config_exists():
        config = cfg_handler.load_config()
    else:
        template_path = Path(__file__).parent / "config_template.yaml"
        cfg_handler.copy_config_template(template_path)
        return

    # Generate sites
    sites = SiteGenerator(
        POSCAR_substrate=Path(config["substrate"]["path"]),
        distance=config["deposit"]["distance"],
        sites=config["substrate"]["sites"]
    ).generate()

    # Generate adsorbates and adsorbate reference points
    adsorbate_generator = AdsorbateGenerator(
        work_mode=config["adsorbate"]["source"],
        path=Path(config["adsorbate"]["path"]),
        pathway_name=config["adsorbate"]["pathway_name"],
        generate_rotations=config["adsorbate"]["rotation"]
    )

    adsorbates = adsorbate_generator.generate_adsorbates(atom_indexes=config["adsorbate"]["atom_indexes"])

    adsorbate_refs = adsorbate_generator.generate_adsorbate_references(
        adsorbates_dict=adsorbates,
        poscar_ads_ref=config["adsorbate"]["reference"]
    )

    # Generate adsorbate-on-site structure files
    structure_generator = AdsorbateDepositor(
        distance=config["deposit"]["distance"],
        POSCAR_substrate=Path(config["substrate"]["path"]),
        sites=sites,
        adsorbates=adsorbates,
        adsorbate_refs=adsorbate_refs
    )

    structures = structure_generator.deposit(
        rotation_generated=config["adsorbate"]["rotation"],
        fix_substrate=config["deposit"]["fix_substrate"],
        target_vacuum_layer=config["deposit"]["target_vacuum_layer"]
    )

    # Write generated models to file
    structure_generator.write(structures, output_dir=Path(config["deposit"]["output_dir"]))

if __name__ == "__main__":
    main()
