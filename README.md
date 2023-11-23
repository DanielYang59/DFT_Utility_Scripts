# DFT Utility Scripts

Collection of Essential Scripts for Density Functional Theory (DFT) Calculations.

## ⚠️ Project Under Development ⚠️

**This project is currently under active development and the scripts have not been fully tested.**

If you find any issues or have suggestions, please [raise an issue](https://github.com/your-repo-link/issues) on this repository.


# Project Structure

```
└── scripts
│       └── vasp
│       │           └── potcar
│       │           └── poscar
│       │           └── kpoints
│       │           └── general
│       └── reaction_diagram_plotter
│       └── adsorbate_depositor
```


# Module Overviews

## reaction_diagram_plotter
Overview not found in scripts/reaction_diagram_plotter/README.md.

## adsorbate_depositor
The `adsorbate_depositor` project is a Python-based tool designed for generating atomic structures with adsorbates deposited on substrate surfaces. It is especially useful for researchers and engineers who work on surface science, catalysis, or computational materials science. This project aims to streamline the process of preparing complex atomic structures for simulation.

## vasp/potcar
This script is designed to generate a POTCAR file used in VASP calculations by reading elements from a POSCAR file and concatenating the corresponding POTCAR files from a given library.

## vasp/poscar
This Python package simplifies the manipulation and management of VASP POSCAR files. It provides convenient scripts and utilities for various tasks, including transferring between Cartesian and Direct coordinate systems, repositioning the entire structure, and adjusting vacuum layer thickness.

## vasp/general
The `vasp_cleanup.py` script is a Python utility designed to clean up unnecessary VASP (Vienna Ab initio Simulation Package) output files in a given directory. The script retains essential input files like `INCAR`, `POSCAR`, `POTCAR`, and `KPOINTS`, along with the job submission script (default is `script.sh`). All other standard VASP output files are moved to a backup directory for safekeeping.

## vasp/kpoints
This Python script generates a regular KPOINTS file for VASP calculations. The user specifies the number of k-points along each of the three axes (`a`, `b`, `c`). They can also choose between a Gamma-centered or Monkhorst-Pack mesh type.


# Contributing to the Project

We welcome contributions from everyone, whether you are an experienced developer or just getting started.


## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.


