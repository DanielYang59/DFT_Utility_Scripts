
# Reaction Diagram Plotter

The **Reaction Diagram Plotter** is a Python tool designed to visualize energy changes in chemical reaction pathways. Given a set of reaction steps and their corresponding energy changes, the plotter generates clear and informative reaction diagrams.

## Folder Structure

* **`example_usage`** : Contains example data files and a script (`runexample.sh`) demonstrating how to use the plotter with predefined data.
  * `intermediate_energies.csv`: CSV file containing intermediate energy data.
  * `reaction_pathway.json`: JSON file containing reaction pathway data.
  * `species_energies.csv`: CSV file containing species energy data.
* **`src`** : Contains the source code files.
  * `diagramPlotter.py`: Module responsible for generating reaction diagram plots.
  * `reactionEnergyCalculator.py`: Module for calculating energy changes in reaction pathways.
  * `energyReader.py`: Module for reading energy data from CSV files.
  * `reactionPathwayParser.py`: Module for parsing reaction pathway data.

## Running the Example

A running example demonstrating the usage of the Reaction Diagram Plotter is provided in the `example_usage` folder. To execute the example, run the following shell script:

```
bash ./example_usage/runexample.sh
```

This script will showcase how to use the plotter with the provided example data files.

## Usage

To use the Reaction Diagram Plotter in your own projects, import the necessary modules from the `src` directory. Provide the reaction steps and their corresponding energy changes as a dictionary to the `DiagramPlotter` class in `diagramPlotter.py`. The plotter will visualize the energy changes and display the plot.
