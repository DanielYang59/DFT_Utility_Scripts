#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Test objectives: Test the free energy calculations of
1. pH=0, external_potential=0:
    a. proton-electron pair (H+ + e-). Expect -3.3836 eV.
    b. hydroxide-electron pair (OH- + e-). Expect -10.0082 eV.

2. pH=0, external_potential=1:
    a. proton-electron pair (H+ + e-). Expect X eV.
    b. hydroxide-electron pair (OH- + e-). Expect X eV.

3. pH=7, external_potential=0:
    a. proton-electron pair (H+ + e-). Expect X eV.
    b. hydroxide-electron pair (OH- + e-). Expect X eV.

"""

import sys
import os

# Append the 'src' directory to the Python path
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'src'))

# Now you can import modules from 'src'
from computationalHydrogenElectrode import ComputationalHydrogenElectrode

# Set up global temperature
temperature = 298.15

if __name__ == "__main__":
    che = ComputationalHydrogenElectrode(temperature=temperature, pH=0, external_potential=0)
    print(che.calculate_proton_free_energy())
    print(che.calculate_hydroxide_free_energy())
