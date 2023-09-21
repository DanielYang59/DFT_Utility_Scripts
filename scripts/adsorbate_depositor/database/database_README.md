# Adsorbate Reaction Pathways Database

## Introduction

This README provides guidelines and explanations for interacting with the Adsorbate Reaction Pathways Database. The database is designed to manage multiple pathways for various chemical reactions, such as CO2RR, HER, OER, and NRR.

## Directory Structure

```lua
|-- CO2RR
|   |-- pathway_database_header.yaml
|-- HER
|   |-- pathway_database_header.yaml
|-- OER
|   |-- pathway_database_header.yaml
|-- NRR
|   |-- pathway_database_header.yaml
|-- README.md
```

## `pathway_database_header.yaml` Format

The `pathway_database_header.yaml` file in each directory contains various pathways in the following structure:

```yaml
pathways:
  pathway_1:
    step_1:
      name: "CO2"
      POSCAR_path: "./POSCAR_CO2"
      adsorbate_atoms: [96, 101, 102]
      reference_atoms: [96, ]
    # Additional steps
  # Additional pathways
```

### Fields

- **pathway_N**: The `N` should be a continuously indexed integer starting from 1. This field contains the steps for a given pathway.
- **step_M**: Similarly, the `M` should also be a continuously indexed integer starting from 1. This field contains the data for a given step within a pathway.
- **name**: The name of the step. Names should be unique within the same `pathway_N`.
- **POSCAR_path**: The relative path to the POSCAR file for the step.
- **adsorbate_atoms**: A list of atoms in the adsorbate, specified by their indices in the POSCAR file (1-indexed).
- **reference_atoms**: A list of atoms that serve as reference points for positioning the adsorbate on the substrate (also 1-indexed). This list should be a subset of `adsorbate_atoms`.

### Rules for Adding Data

1. `pathway_N` should be indexed continuously from 1 and should not have duplicates.
2. `step_M` within each `pathway_N` should also be indexed continuously from 1 and should not have duplicates.
3. Different steps should not have the same `name` tag within the same `pathway_N`.
4. The `reference_atoms` should be a subset (or the same set) of `adsorbate_atoms`.
5. Neither `adsorbate_atoms` nor `reference_atoms` should be empty, should contain only non-negative integers, and should not have duplicates.

## Contributing

To add a new chemical reaction or pathway, create a new directory for the reaction (if it doesn't exist) and add a `pathway_database_header.yaml` file that follows the format and rules described above.
