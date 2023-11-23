#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pathlib import Path

from src.userConfigParser import UserConfigParser
from src.vasprunXmlReader import VasprunXmlReader
from src.outputPdosGenerator import OutputPdosGenerator

def main(configfile=Path("PDOSIN")):
    # Get current working directory
    cwd = Path.cwd()

    # Read config file
    config_parser = UserConfigParser(configfile=cwd / configfile)

    if not configfile.is_file():  # or generate config template
        config_parser.generate_config_template()

    config_parser.read_config()

    # Get requested curve list
    requested_curves = config_parser.parse()

    # Import vasprun.xml file
    vasprunxml_reader = VasprunXmlReader(vasprunXmlFile=cwd / "vasprun.xml")

    ## Read fermi level and ISPIN tag from vasprun.xml
    ispin = vasprunxml_reader.read_incar_tag(tag="ISPIN")
    fermi_level = vasprunxml_reader.read_fermi_level()

    # For each curve required, fetch PDOS data
    fetched_pdos_data = [
        vasprunxml_reader.read_curve(curve_info=requested_curve)
        for requested_curve in requested_curves
        ]

    # Fetch energy data
    energies = vasprunxml_reader.read_energies()
    energies -= fermi_level

    # Output fetched PDOS data
    output_generator = OutputPdosGenerator(fetched_pdos_data, energies)
    output_generator.write(cwd / "PDOS.dat")

if __name__ == "__main__":
    main()
