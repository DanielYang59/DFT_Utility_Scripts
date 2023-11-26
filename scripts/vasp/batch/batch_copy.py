#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
from pathlib import Path
import shutil

from lib.list_vasp_dir import list_vasp_dirs

def main():
    """
    Copy specified files to all valid VASP directories.

    The function uses argparse to parse command-line arguments and expects
    a list of file paths to copy to VASP directories.

    Raises:
        FileNotFoundError: If any of the specified files do not exist.

    Note:
        The VASP directories are determined using the list_vasp_dirs function
      from the lib.list_vasp_dir module.
    """
    # Create argument parser
    parser = argparse.ArgumentParser(description="Copy files to all valid VASP directories.")

    # Add the positional argument for files to copy
    parser.add_argument("files", metavar="file", nargs="+", help="Files to copy to VASP directories.")

    # Parse command-line arguments
    args = parser.parse_args()

    # Check if each specified file exists
    for file_path in args.files:
        if not Path(file_path).is_file():
            raise FileNotFoundError(f"Cannot find file {file_path}.")

    # List VASP dirs under cwd
    vasp_dirs = list_vasp_dirs(Path.cwd())

    # Copy files to each VASP directory
    for vasp_dir in vasp_dirs:
        for file_path in args.files:
            shutil.copy(file_path, vasp_dir)

if __name__ == "__main__":
    main()
