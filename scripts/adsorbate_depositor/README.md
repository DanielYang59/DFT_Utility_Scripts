# Adsorbate Depositor

## Overview

The `adsorbate_depositor` project is a Python-based tool designed for generating atomic structures with adsorbates deposited on substrate surfaces. It is especially useful for researchers and engineers who work on surface science, catalysis, or computational materials science. This project aims to streamline the process of preparing complex atomic structures for simulation.

## Features

* **Configurable Settings** : Customize deposition settings via a YAML-based configuration file.
* **Multiple Site Support** : Supports various adsorption sites on the substrate.
* **Adsorbate Rotation** : Automatically generate rotated versions of adsorbates.
* **File Output** : Outputs the generated structure in VASP POSCAR format.

## Workflow

1. **Load Configuration** : The script starts by reading a `config.yaml` file located in the current working directory. If the configuration file is not found, a template configuration will be generated for you.
2. **Generate Site** : In this step, the script identifies and prepares the sites on the substrate where the adsorbates will be deposited.
3. **Generate Adsorbate** : Based on the settings in the `config.yaml`, the script will generate the adsorbate structures to be used.
4. **Adsorbate Deposition** : The adsorbates generated are then deposited onto the pre-selected sites on the substrate.
5. **Distance Adjustment** : Finally, the script adjusts the minimum distance between the adsorbate and the substrate based on the preset value in the `config.yaml`.

## Installation

Clone this repository to your local machine.

```bash
git clone https://github.com/yourusername/adsorbate_depositor.git
```

Navigate to the cloned directory and install the required packages.

## Directory Structure

```css
adsorbate_depositor/
├── README.md
├── config_template.yaml
├── database/
│   ├── CO2RR/
│   ├── HER/
│   └── NITRR/
├── main.py
└── src/
    ├── adsorbateDepositor.py
    ├── adsorbateGenerator.py
    ├── configHandler.py
    └── siteGenerator.py
```
