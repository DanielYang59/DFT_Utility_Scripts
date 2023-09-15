
# DFT Utility Scripts

Collection of Essential Scripts for Density Functional Theory (DFT) Calculations

## general

# VASP Cleanup Script

## Overview

The `vasp_cleanup.py` script is a Python utility designed to clean up unnecessary VASP (Vienna Ab initio Simulation Package) output files in a given directory. The script retains essential input files like `INCAR`, `POSCAR`, `POTCAR`, and `KPOINTS`, along with the job submission script (default is `script.sh`). All other standard VASP output files are moved to a backup directory for safekeeping.

## Requirements

- Python 3.x
- No external Python packages are required.

## Features

- Moves standard VASP output files to a backup directory.
- Creates a new backup directory if previous ones exist.
- Provides an optional verbosity setting for console output.

## Usage

1. Navigate to the directory containing your VASP files in a terminal.
2. Run the script by specifying its full path:

   ```
   python3 /path/to/vasp_cleanup.py
   ```

### Optional Parameters

- `--job_script`: The name of the job submission script you'd like to keep. Default is `script.sh`.
- `--verbose`: Sets the verbosity level. Can be either "silent" or "verbose". Default is "silent".

### Example Usage from Python

If you prefer to call the script's function from within another Python script, you can do so like this:

```python
from pathlib import Path
from vasp_cleanup import clean_vasp_files

directory = Path(os.getcwd())
clean_vasp_files(directory, job_script="my_script.sh", verbose="verbose")
```

## doscar

## potcar

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

## kpoints

# VASP KPOINTS File Generator

## Overview

This Python script generates a regular KPOINTS file for VASP calculations. The user specifies the number of k-points along each of the three axes (`a`, `b`, `c`). They can also choose between a Gamma-centered or Monkhorst-Pack mesh type.

## Requirements

- Python 3.x

## Usage

### Syntax

```bash
python3 kpoints.py <a> <b> <c> [-m <mesh_type_initial>]
```

## cohp

## reaction_diagram

# Reaction Diagram Plotter

## Overview

The Reaction Diagram Plotter is a Python-based tool that generates reaction pathway diagrams using free energy changes (Delta G) for each reaction step. The tool outputs a `.png` file that visualizes the reaction pathway.

## Features

- Configurable plot aesthetics, including line thickness, axis labels, and tick marks
- Reads input from CSV files for molecular species and intermediates, and from JSON for reaction data
- Built-in calculation for free energy changes of each step in the reaction pathway
- Output directory can be specified

## Dependencies

- Python 3.x
- matplotlib
- pathlib

## Installation

Clone the repository to your local machine:

\```bash
git clone https://github.com/your-username/reaction-diagram-plotter.git
\```

Install the required Python packages:

\```bash
pip install matplotlib
\```

## Usage

1. Add your molecular species data to `data/molecular_species_energy.csv`.
2. Add your intermediates data to `data/intermediate_energy.csv`.
3. Add your reaction pathway data to `data/reaction.json`.

Run the main script:

\```bash
python main.py
\```

By default, the output will be saved in an `output` folder in `.png` format.

## Contributing

Contributions are welcome. Please open an issue or create a pull request with your changes.

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## general

# VASP Cleanup Script

## Overview

The `vasp_cleanup.py` script is a Python utility designed to clean up unnecessary VASP (Vienna Ab initio Simulation Package) output files in a given directory. The script retains essential input files like `INCAR`, `POSCAR`, `POTCAR`, and `KPOINTS`, along with the job submission script (default is `script.sh`). All other standard VASP output files are moved to a backup directory for safekeeping.

## Requirements

- Python 3.x
- No external Python packages are required.

## Features

- Moves standard VASP output files to a backup directory.
- Creates a new backup directory if previous ones exist.
- Provides an optional verbosity setting for console output.

## Usage

1. Navigate to the directory containing your VASP files in a terminal.
2. Run the script by specifying its full path:

   ```
   python3 /path/to/vasp_cleanup.py
   ```

### Optional Parameters

- `--job_script`: The name of the job submission script you'd like to keep. Default is `script.sh`.
- `--verbose`: Sets the verbosity level. Can be either "silent" or "verbose". Default is "silent".

### Example Usage from Python

If you prefer to call the script's function from within another Python script, you can do so like this:

```python
from pathlib import Path
from vasp_cleanup import clean_vasp_files

directory = Path(os.getcwd())
clean_vasp_files(directory, job_script="my_script.sh", verbose="verbose")
```

### Comments

<!-- Add comments about this script here. -->

## doscar

### Comments

<!-- Add comments about this script here. -->

## potcar

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

### Comments

<!-- Add comments about this script here. -->

## kpoints

# VASP KPOINTS File Generator

## Overview

This Python script generates a regular KPOINTS file for VASP calculations. The user specifies the number of k-points along each of the three axes (`a`, `b`, `c`). They can also choose between a Gamma-centered or Monkhorst-Pack mesh type.

## Requirements

- Python 3.x

## Usage

### Syntax

```bash
python3 kpoints.py <a> <b> <c> [-m <mesh_type_initial>]
```

### Comments

<!-- Add comments about this script here. -->

## cohp

### Comments

<!-- Add comments about this script here. -->

## reaction_diagram

# Reaction Diagram Plotter

## Overview

The Reaction Diagram Plotter is a Python-based tool that generates reaction pathway diagrams using free energy changes (Delta G) for each reaction step. The tool outputs a `.png` file that visualizes the reaction pathway.

## Features

- Configurable plot aesthetics, including line thickness, axis labels, and tick marks
- Reads input from CSV files for molecular species and intermediates, and from JSON for reaction data
- Built-in calculation for free energy changes of each step in the reaction pathway
- Output directory can be specified

## Dependencies

- Python 3.x
- matplotlib
- pathlib

## Installation

Clone the repository to your local machine:

\```bash
git clone https://github.com/your-username/reaction-diagram-plotter.git
\```

Install the required Python packages:

\```bash
pip install matplotlib
\```

## Usage

1. Add your molecular species data to `data/molecular_species_energy.csv`.
2. Add your intermediates data to `data/intermediate_energy.csv`.
3. Add your reaction pathway data to `data/reaction.json`.

Run the main script:

\```bash
python main.py
\```

By default, the output will be saved in an `output` folder in `.png` format.

## Contributing

Contributions are welcome. Please open an issue or create a pull request with your changes.

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

### Comments

<!-- Add comments about this script here. -->

## Table of Contents

- [general](#general)
- [doscar](#doscar)
- [potcar](#potcar)
- [kpoints](#kpoints)
- [cohp](#cohp)
- [reaction_diagram](#reaction_diagram)

## general

# VASP Cleanup Script

## Overview

The `vasp_cleanup.py` script is a Python utility designed to clean up unnecessary VASP (Vienna Ab initio Simulation Package) output files in a given directory. The script retains essential input files like `INCAR`, `POSCAR`, `POTCAR`, and `KPOINTS`, along with the job submission script (default is `script.sh`). All other standard VASP output files are moved to a backup directory for safekeeping.

## Requirements

- Python 3.x
- No external Python packages are required.

## Features

- Moves standard VASP output files to a backup directory.
- Creates a new backup directory if previous ones exist.
- Provides an optional verbosity setting for console output.

## Usage

1. Navigate to the directory containing your VASP files in a terminal.
2. Run the script by specifying its full path:

   ```
   python3 /path/to/vasp_cleanup.py
   ```

### Optional Parameters

- `--job_script`: The name of the job submission script you'd like to keep. Default is `script.sh`.
- `--verbose`: Sets the verbosity level. Can be either "silent" or "verbose". Default is "silent".

### Example Usage from Python

If you prefer to call the script's function from within another Python script, you can do so like this:

```python
from pathlib import Path
from vasp_cleanup import clean_vasp_files

directory = Path(os.getcwd())
clean_vasp_files(directory, job_script="my_script.sh", verbose="verbose")
```

## doscar

## potcar

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

## kpoints

# VASP KPOINTS File Generator

## Overview

This Python script generates a regular KPOINTS file for VASP calculations. The user specifies the number of k-points along each of the three axes (`a`, `b`, `c`). They can also choose between a Gamma-centered or Monkhorst-Pack mesh type.

## Requirements

- Python 3.x

## Usage

### Syntax

```bash
python3 kpoints.py <a> <b> <c> [-m <mesh_type_initial>]
```

## cohp

## reaction_diagram

# Reaction Diagram Plotter

## Overview

The Reaction Diagram Plotter is a Python-based tool that generates reaction pathway diagrams using free energy changes (Delta G) for each reaction step. The tool outputs a `.png` file that visualizes the reaction pathway.

## Features

- Configurable plot aesthetics, including line thickness, axis labels, and tick marks
- Reads input from CSV files for molecular species and intermediates, and from JSON for reaction data
- Built-in calculation for free energy changes of each step in the reaction pathway
- Output directory can be specified

## Dependencies

- Python 3.x
- matplotlib
- pathlib

## Installation

Clone the repository to your local machine:

\```bash
git clone https://github.com/your-username/reaction-diagram-plotter.git
\```

Install the required Python packages:

\```bash
pip install matplotlib
\```

## Usage

1. Add your molecular species data to `data/molecular_species_energy.csv`.
2. Add your intermediates data to `data/intermediate_energy.csv`.
3. Add your reaction pathway data to `data/reaction.json`.

Run the main script:

\```bash
python main.py
\```

By default, the output will be saved in an `output` folder in `.png` format.

## Contributing

Contributions are welcome. Please open an issue or create a pull request with your changes.

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

<!-- TOC -->

- [DFT_scripts](#dft_scripts)
  - [general](#general)
- [VASP Cleanup Script](#vasp-cleanup-script)
  - [Overview](#overview)
  - [Requirements](#requirements)
  - [Features](#features)
  - [Usage](#usage)
    - [Optional Parameters](#optional-parameters)
    - [Example Usage from Python](#example-usage-from-python)
  - [doscar](#doscar)
  - [potcar](#potcar)
- [POTCAR Generation Script](#potcar-generation-script)
  - [Overview](#overview)
  - [Requirements](#requirements)
  - [Directory Structure](#directory-structure)
  - [Usage](#usage)
    - [Optional: Specifying a Custom POSCAR File](#optional:-specifying-a-custom-poscar-file)
  - [Functions](#functions)
  - [Testing](#testing)
  - [kpoints](#kpoints)
- [VASP KPOINTS File Generator](#vasp-kpoints-file-generator)
  - [Overview](#overview)
  - [Requirements](#requirements)
  - [Usage](#usage)
    - [Syntax](#syntax)
  - [cohp](#cohp)
  - [reaction_diagram](#reaction_diagram)
- [Reaction Diagram Plotter](#reaction-diagram-plotter)
  - [Overview](#overview)
  - [Features](#features)
  - [Dependencies](#dependencies)
  - [Installation](#installation)
  - [Usage](#usage)
  - [Contributing](#contributing)
  - [License](#license)
  - [general](#general)
- [VASP Cleanup Script](#vasp-cleanup-script)
  - [Overview](#overview)
  - [Requirements](#requirements)
  - [Features](#features)
  - [Usage](#usage)
    - [Optional Parameters](#optional-parameters)
    - [Example Usage from Python](#example-usage-from-python)
    - [Comments](#comments)
  - [doscar](#doscar)
    - [Comments](#comments)
  - [potcar](#potcar)
- [POTCAR Generation Script](#potcar-generation-script)
  - [Overview](#overview)
  - [Requirements](#requirements)
  - [Directory Structure](#directory-structure)
  - [Usage](#usage)
    - [Optional: Specifying a Custom POSCAR File](#optional:-specifying-a-custom-poscar-file)
  - [Functions](#functions)
  - [Testing](#testing)
    - [Comments](#comments)
  - [kpoints](#kpoints)
- [VASP KPOINTS File Generator](#vasp-kpoints-file-generator)
  - [Overview](#overview)
  - [Requirements](#requirements)
  - [Usage](#usage)
    - [Syntax](#syntax)
    - [Comments](#comments)
  - [cohp](#cohp)
    - [Comments](#comments)
  - [reaction_diagram](#reaction_diagram)
- [Reaction Diagram Plotter](#reaction-diagram-plotter)
  - [Overview](#overview)
  - [Features](#features)
  - [Dependencies](#dependencies)
  - [Installation](#installation)
  - [Usage](#usage)
  - [Contributing](#contributing)
  - [License](#license)
    - [Comments](#comments)
  - [Table of Contents](#table-of-contents)
  - [general](#general)
- [VASP Cleanup Script](#vasp-cleanup-script)
  - [Overview](#overview)
  - [Requirements](#requirements)
  - [Features](#features)
  - [Usage](#usage)
    - [Optional Parameters](#optional-parameters)
    - [Example Usage from Python](#example-usage-from-python)
  - [doscar](#doscar)
  - [potcar](#potcar)
- [POTCAR Generation Script](#potcar-generation-script)
  - [Overview](#overview)
  - [Requirements](#requirements)
  - [Directory Structure](#directory-structure)
  - [Usage](#usage)
    - [Optional: Specifying a Custom POSCAR File](#optional:-specifying-a-custom-poscar-file)
  - [Functions](#functions)
  - [Testing](#testing)
  - [kpoints](#kpoints)
- [VASP KPOINTS File Generator](#vasp-kpoints-file-generator)
  - [Overview](#overview)
  - [Requirements](#requirements)
  - [Usage](#usage)
    - [Syntax](#syntax)
  - [cohp](#cohp)
  - [reaction_diagram](#reaction_diagram)
- [Reaction Diagram Plotter](#reaction-diagram-plotter)
  - [Overview](#overview)
  - [Features](#features)
  - [Dependencies](#dependencies)
  - [Installation](#installation)
  - [Usage](#usage)
  - [Contributing](#contributing)
  - [License](#license)

<!-- /TOC -->

## general

# VASP Cleanup Script

## Overview

The `vasp_cleanup.py` script is a Python utility designed to clean up unnecessary VASP (Vienna Ab initio Simulation Package) output files in a given directory. The script retains essential input files like `INCAR`, `POSCAR`, `POTCAR`, and `KPOINTS`, along with the job submission script (default is `script.sh`). All other standard VASP output files are moved to a backup directory for safekeeping.

## Requirements

- Python 3.x
- No external Python packages are required.

## Features

- Moves standard VASP output files to a backup directory.
- Creates a new backup directory if previous ones exist.
- Provides an optional verbosity setting for console output.

## Usage

1. Navigate to the directory containing your VASP files in a terminal.
2. Run the script by specifying its full path:

   ```
   python3 /path/to/vasp_cleanup.py
   ```

### Optional Parameters

- `--job_script`: The name of the job submission script you'd like to keep. Default is `script.sh`.
- `--verbose`: Sets the verbosity level. Can be either "silent" or "verbose". Default is "silent".

### Example Usage from Python

If you prefer to call the script's function from within another Python script, you can do so like this:

```python
from pathlib import Path
from vasp_cleanup import clean_vasp_files

directory = Path(os.getcwd())
clean_vasp_files(directory, job_script="my_script.sh", verbose="verbose")
```

## doscar

## potcar

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

## kpoints

# VASP KPOINTS File Generator

## Overview

This Python script generates a regular KPOINTS file for VASP calculations. The user specifies the number of k-points along each of the three axes (`a`, `b`, `c`). They can also choose between a Gamma-centered or Monkhorst-Pack mesh type.

## Requirements

- Python 3.x

## Usage

### Syntax

```bash
python3 kpoints.py <a> <b> <c> [-m <mesh_type_initial>]
```

## cohp

## reaction_diagram

# Reaction Diagram Plotter

## Overview

The Reaction Diagram Plotter is a Python-based tool that generates reaction pathway diagrams using free energy changes (Delta G) for each reaction step. The tool outputs a `.png` file that visualizes the reaction pathway.

## Features

- Configurable plot aesthetics, including line thickness, axis labels, and tick marks
- Reads input from CSV files for molecular species and intermediates, and from JSON for reaction data
- Built-in calculation for free energy changes of each step in the reaction pathway
- Output directory can be specified

## Dependencies

- Python 3.x
- matplotlib
- pathlib

## Installation

Clone the repository to your local machine:

\```bash
git clone https://github.com/your-username/reaction-diagram-plotter.git
\```

Install the required Python packages:

\```bash
pip install matplotlib
\```

## Usage

1. Add your molecular species data to `data/molecular_species_energy.csv`.
2. Add your intermediates data to `data/intermediate_energy.csv`.
3. Add your reaction pathway data to `data/reaction.json`.

Run the main script:

\```bash
python main.py
\```

By default, the output will be saved in an `output` folder in `.png` format.

## Contributing

Contributions are welcome. Please open an issue or create a pull request with your changes.

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.
