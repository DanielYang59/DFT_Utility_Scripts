# Adsorbate Depositor

## Overview

The `adsorbate_depositor` project is a Python-based tool designed for generating atomic structures with adsorbates deposited on substrate surfaces. It is especially useful for researchers and engineers who work on surface science, catalysis, or computational materials science. This project aims to streamline the process of preparing complex atomic structures for simulation.

## Features

- **Configurable Settings**: Customize deposition settings via a YAML-based configuration file.
- **Multiple Site Support**: Supports various adsorption sites on the substrate.
- **Adsorbate Rotation**: Automatically generate rotated versions of adsorbates.
- **File Output**: Outputs the generated structure in VASP POSCAR format.

## Installation

Clone this repository to your local machine.

```bash
git clone https://github.com/yourusername/adsorbate_depositor.git
```

Navigate to the cloned directory and install the required packages.

## Usage

Run the `main.py` script to start the generation process.

```bash
python main.py
```

## Directory Structure

* `src/`: Contains the source code for the project.
  * `configHandler.py`: Manages reading and writing of configuration files.
  * `adsorbateGenerator.py`: Responsible for generating adsorbate structures.
  * `siteGenerator.py`: Generates various adsorption sites on the substrate.
  * `adsorbateDepositor.py`: Handles the deposition of adsorbates onto the substrate at specified sites.

## Contributing

If you'd like to contribute, please fork the repository and make changes as you'd like. Pull requests are warmly welcome.
