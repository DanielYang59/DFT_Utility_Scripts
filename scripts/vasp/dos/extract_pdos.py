#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pathlib import Path

from src.userConfigParser import UserConfigParser
from src.vasprunXmlReader import VasprunXmlReader
from src.outputPdosGenerator import OutputPdosGenerator

def main(configfile=Path("PDOSIN")) -> None:
    """
    Main function for extracting Partial Density of States (PDOS) data from vasprun.xml file.

    Parameters:
        configfile (Path, optional): Path to the configuration file (PDOSIN). Defaults to "PDOSIN" in the current working directory.

    Returns:
        None

    This function reads the configuration file, parses the requested curves, imports the vasprun.xml file,
    reads the Fermi level and ISPIN tag, and fetches PDOS data for each requested curve.
    The fetched PDOS data, along with energy data, is then written to the output file "PDOS.dat" in the current working directory.
    If the specified configuration file does not exist, a config template is generated.

    Note: The PDOSIN configuration file specifies the curves for which PDOS data should be generated.
    The vasprun.xml file is assumed to be present in the current working directory.

    """
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
    ispin = vasprunxml_reader.read_incar_tag(tag="ISPIN")  # TODO: need to consider ispin = 1
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
