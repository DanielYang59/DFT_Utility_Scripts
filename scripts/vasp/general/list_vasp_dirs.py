#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pathlib import Path
from typing import List

from .is_vasp_dir import is_vasp_dir

def list_vasp_dirs(parent_dir: Path) ->List[Path]:
    """
    Retrieve a list of valid VASP directories under the specified parent directory.

    Parameters:
        parent_dir (Path): The parent directory to search for valid VASP directories.

    Returns:
        list: A list of Path objects representing valid VASP directories.

    Raises:
        ValueError: If the specified parent directory is not a valid directory.
    """
    valid_vasp_dirs = []

    # Check if parent_dir is a directory
    if not parent_dir.is_dir():
        raise ValueError("The specified parent directory is not a valid directory.")

    for dir_path in parent_dir.iterdir():
        if dir_path.is_dir() and is_vasp_dir(dir_path):
            valid_vasp_dirs.append(dir_path)

    return valid_vasp_dirs

if __name__ == "__main__":
    list_vasp_dirs(Path.cwd())
