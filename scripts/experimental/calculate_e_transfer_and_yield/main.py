#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pathlib import Path

from src.configParser import YAMLConfigParser
from src.calculate_e_transfer_and_yield import Calculator
from src.plotter import e_transfer_and_yield_plotter

def main():
    # Load config
    configParser = YAMLConfigParser(
        config_file_path=Path.cwd() / "config.yaml",
        template_file_path=Path(__file__).resolve().parent / "config_template.yaml"
        )
    config = configParser.load_yaml()


    # Calculate electronic transfer number and H2O2 yield
    data = {}
    for sample_name in config["dataExtract"]["samples"]:
        # Initialize calculator
        calculator = Calculator(
            sample_name=sample_name,
            disk_suffix=config["dataExtract"]["disk_suffix"],
            ring_suffix=config["dataExtract"]["ring_suffix"],
            constant_N=config["calculation"]["N"]
            )

        # Prepare values for plotting
        data[sample_name] = [
            calculator.extract_potential(source="disk", offset=config["calculation"]["e_offset"]),
            calculator.calculate_yield(),
            calculator.calculate_e_transfer(),
            ]

    # Pass curves data into plotter for plotting
    plotter = e_transfer_and_yield_plotter(data, config["plotting"])
    plotter.plot()

if __name__ == "__main__":
    main()
