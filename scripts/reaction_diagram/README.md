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

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
