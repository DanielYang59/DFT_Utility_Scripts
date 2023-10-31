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
    config_parser = VasprunXmlReader(configfile=configfile)
    
    if configfile.is_file():
        config_parser.read_config()
        
    
    # or generate config template (and exist)
    else:
        config_parser.generate_config_template()


    # Import vasprun.xml file
    vasprunxml_reader = VasprunXmlReader()
    
    ## Read fermi level and ispin
    fermi_level = vasprunxml_reader 
    
    
    # For each curve required, fetch PDOS data
    
    
    # Output fetched PDOS data


if __name__ == "__main__":
    main()
