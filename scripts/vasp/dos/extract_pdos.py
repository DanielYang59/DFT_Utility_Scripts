#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pathlib import Path
import sys

from src.userConfigParser import UserConfigParser
from src.vasprunXmlReader import VasprunXmlReader
from src.pdosCurveFetcher import PdosCurveFetcher
from src.write_output_pdos import write_pdos_to_file

def main(configfile=Path("PDOSIN")) -> None:
    """
    Main function for extracting Partial Density of States (PDOS) data from vasprun.xml file.

    Parameters:
        configfile (Union[str, Path], optional): Path to the configuration file (PDOSIN).
            Defaults to "PDOSIN" in the current working directory.

    This function reads the configuration file, parses the requested curves, imports the vasprun.xml file,
    reads the Fermi level and ISPIN tag, and fetches PDOS data for each requested curve.
    The fetched PDOS data, along with energy data, is then written to the output file "PDOS.csv" in the current working directory.
    If the specified configuration file does not exist, a config template is generated.

    Note: The PDOSIN configuration file specifies the curves for which PDOS data should be generated.
    The vasprun.xml file is assumed to be present in the current working directory.

    """
    # Get current working directory
    cwd = Path.cwd()


    # Import vasprun.xml file
    print("Importing vasprun.xml file......")
    vasprunxml_reader = VasprunXmlReader(vasprunXmlFile=cwd / "vasprun.xml")

    fermi_level = vasprunxml_reader.read_fermi_level()
    atom_list = vasprunxml_reader.read_atom_list()
    ispin = int(vasprunxml_reader.read_incar_tag("ISPIN"))


    # Read config file
    config_parser = UserConfigParser(configfile=cwd / configfile)

    if configfile.is_file():
        requested_curves = config_parser.read_config(atom_list)

    # or generate config template if not existing
    else:
        config_parser.generate_config_template(Path(__file__).resolve().parent / "src" / "PDOSIN.template")
        sys.exit("PDOSIN not found. Template generated.")


    # For each curve required, fetch PDOS data
    fetcher = PdosCurveFetcher(vasprunxml_reader)
    pdos_data = [fetcher.fetch_curve(curve, ispin) for curve in requested_curves]

    # Output PDOS data (and reference energy to fermi level)
    write_pdos_to_file(pdos_data, fermi_level, cwd / "PDOS.csv")
    print("Done! pDOS written to PDOS.csv file.")

if __name__ == "__main__":
    main()
