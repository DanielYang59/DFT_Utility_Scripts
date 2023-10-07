# POSCAR Utility Library for VASP Calculations

## Overview

This Python package simplifies the manipulation and management of VASP POSCAR files. It provides convenient scripts and utilities for various tasks, including transferring between Cartesian and Direct coordinate systems, repositioning the entire structure, and adjusting vacuum layer thickness.

## Directory Structure

```bash
.
├── coordinate_system_transfer.py
├── lib
│   ├── atomSelector.py
│   ├── find_or_request_poscar.py
│   ├── read_poscar.py
│   └── write_poscar.py
├── structureRepositioner.py
└── vacuumLayerManager.py

```

## Scripts and Utilities

### 1. Coordinate System Transfer (`coordinate_system_transfer.py`)

This script allows you to seamlessly transfer atomic coordinates between Cartesian and Direct coordinate systems, ensuring consistency in your VASP simulations.

### 2. Structure Repositioner (`structureRepositioner.py`)

The `structureRepositioner.py` script provides functionality to move the entire atomic structure along specified axes. This is particularly useful for adjusting the position of the entire system according to your simulation requirements.

### 3. Vacuum Layer Manager (`vacuumLayerManager.py`)

The `vacuumLayerManager.py` script facilitates the adjustment of vacuum layer thickness in your simulation cell. It allows you to modify the empty space between periodic images, crucial for accurate surface calculations and preventing artificial interactions between periodic replicas.

## Usage

Each script in the package can be utilized independently for specific tasks. Detailed instructions for using each script can be found in their respective Python files.

## Requirements

- Python 3.x

## Usage Example

```bash
python3 coordinate_system_transfer.py
python3 structureRepositioner.py
python3 vacuumLayerManager.py
```

## Feel free to explore and utilize the provided scripts to streamline your VASP simulations.

Feel free to copy and use this content in your README file! If you need any further modifications or additions, please let me know!
