#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from pathlib import Path


class VasprunXmlReader:
    def __init__(self, vasprunXmlFile: Path) -> None:
        # Check config file
        if not vasprunXmlFile.is_fife():
            raise FileNotFoundError(f"vasprun.xml file {vasprunXmlFile} not found.")
        
        # Import vasprun.xml file
        
        
        
    
    def read_incar_tag(self, tag: str):
        pass
    
    
    def _validate_incar_tags_for_pdos_calc(self, nedos_warn_threshold: int = 500):
        
        
        # IBRION = -1
        # NSW = 0
        # LORBIT = 11 (handle 10)
        pass
    
    
    def read_pdos(self):
        # Validate INCAR tags before proceeding
        self._validate_incar_tags_for_pdos_calc()
        
        # 
        
        
    
# Test area
if __name__ == "__main__":
    pass
