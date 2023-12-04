#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# TODO: retest after adding vacuum layer detection

import sys
from pathlib import Path
from ase.io import read, write

script_dir = Path(__file__).resolve().parent
sys_path_to_append = script_dir.parents[5] / "Developer/DFT_Utility_Scripts/scripts/vasp/poscar"
sys.path.append(str(sys_path_to_append))

from structureRepositioner import StructureRepositioner

def test_reposition_atoms(test_data_path: Path, output_path: Path):
    """
    Test the StructureRepositioner by applying all nine transformations
    to the test POSCAR files.

    Parameters:
        test_data_path (Path): The directory containing the test POSCAR files.
        output_path (Path): The directory where the modified POSCAR files will be saved.
    """
    axes = ['x', 'y', 'z']
    modes = ['min_bound', 'center', 'max_bound']

    for axis in axes:
        for mode in modes:
            poscar_file = test_data_path / f"POSCAR_graphene_offset_{axis}"
            structure = read(poscar_file, format="vasp")

            repositioner = StructureRepositioner(structure, axis=axis)
            repositioner.reposition_along_axis(mode=mode)

            output_file = output_path / f"POSCAR_graphene_moved_{mode}_{axis}"
            write(output_file, repositioner.structure, format="vasp")

if __name__ == "__main__":
    test_data_path = Path("test_data")
    output_path = Path("test_output")
    output_path.mkdir(exist_ok=True)

    test_reposition_atoms(test_data_path, output_path)
