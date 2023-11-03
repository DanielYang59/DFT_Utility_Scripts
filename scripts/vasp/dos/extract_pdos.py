#!/usr/bin/env python3
# -*- coding: utf-8 -*-


""" Brief Intro:  # DEBUG: remove after refactoring
Generate PDOS data from "vasprun.xml" file, by YangHy.
If you find this script helpful or have any issue/advice to report,
you could kindly reach out to me at yanghaoyu97@outlook.com.
Deeply appreciate the help from Mr. WANG Qiankun and the advice from Dr. ZHAO Juanli.
"""


from pathlib import Path

from src.userConfigParser import UserConfigParser
from src.vasprunXmlReader import VasprunXmlReader
from src.outputPdosGenerator import OutputPdosGenerator


def main(configfile=Path("PDOSIN")):  # NOTE: rewrite to current working dir
    # Read config file 
    config_parser = UserConfigParser(configfile=configfile)
    
    if not configfile.is_file():  # or generate config template
        config_parser.generate_config_template()
    
    config_parser.read_config()
    
    # Get requested curve list
    requested_curves = config_parser.parse()


    # Import vasprun.xml file
    vasprunxml_reader = VasprunXmlReader(vasprunXmlFile="vasprun.xml")  # NOTE: rewrite to current working dir
    
    ## Read fermi level and ISPIN tag
    # TODO: read fermi level
    ispin = vasprunxml_reader.read_incar_tag(tag="ISPIN")
    
    
    # For each curve required, fetch PDOS data
    fetched_pdos_data = [
        vasprunxml_reader.read_curve(curve_info=requested_curve)
        for requested_curve in requested_curves
        ]
    
    
    # TODO: remember to insert energy data
    
    
    # Output fetched PDOS data
    output_generator = OutputPdosGenerator(fetched_pdos_data)


if __name__ == "__main__":
    main()
