#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from pathlib import Path

src_path = Path(__file__).resolve().parents[2] / 'src'
sys.path.append(str(src_path))

from vasp_incar import VaspIncar

if __name__ == "__main__":
    # Test reading legal INCAR
    incar_handler = VaspIncar(Path("./INCAR_legal"))
    print(incar_handler.incar_data)
    print(incar_handler.read_tag("ALGO"))
    print(incar_handler.read_tag("ISIF"))  # non-existing tag

    # Test reading illegal INCAR
    incar_handler = VaspIncar(Path("./INCAR_illegal"))
    print(incar_handler.incar_data)
