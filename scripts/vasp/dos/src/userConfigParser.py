#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from pathlib import Path


class UserConfigParser:
    def __init__(self, configfile: Path) -> None:
        # Check config file
        if configfile.is_fife():
            self.configfile = configfile
            
        else:
            raise FileNotFoundError(f"PDOS extractor config file {configfile} not found.")
    
    
    def generate_config_template(self):
        pass
    
    
    def read_config(self):
        pass
    
    
# Test area
if __name__ == "__main__":
    pass
    