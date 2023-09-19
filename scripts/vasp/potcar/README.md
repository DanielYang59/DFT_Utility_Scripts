# POTCAR Generation Script

## Overview

This script is designed to generate a POTCAR file used in VASP calculations by reading elements from a POSCAR file and concatenating the corresponding POTCAR files from a given library.

## Requirements

- Python 3.x
- Your operating system should have an environment variable named `POTCAR_LIBRARY_PATH` set to the path of your POTCAR library.

## Directory Structure

The project is structured as follows:

\`\`\`
ROOT/
├── scripts/
│   └── potcar/
│       └── generate_potcar.py
└── tests/
    └── potcar/
        ├── __init__.py
        ├── test_generate_potcar.py
        └── potcar_lib/
\`\`\`

## Usage

Run the script in the terminal like so:

\`\`\`bash
python generate_potcar.py
\`\`\`

This will read the POSCAR file in the current directory, look for the required POTCAR files in the directory specified by `POTCAR_LIBRARY_PATH`, and then generate a new POTCAR file in the current directory.

### Optional: Specifying a Custom POSCAR File

You can optionally specify the path to a POSCAR file:

\`\`\`bash
python generate_potcar.py --poscarfile /path/to/your/POSCAR
\`\`\`

## Functions

- `generate_potcar(potcar_lib, elements, output_potcarfile=Path("POTCAR"))`

  - Generates a POTCAR file based on the elements list.
- `get_elements_from_poscar(poscarfile)`

  - Reads the element types from a given POSCAR file.
- `get_potcar_library_path()`

  - Fetches the POTCAR library path from the environment variable `POTCAR_LIBRARY_PATH`.

## Testing

To run the tests, navigate to
