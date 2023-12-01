#!/bin/bash
# -*- coding: utf-8 -*-

# Define external potential (V) and pH
EXTERNAL_POTENTIAL=0
PH=0

# Call the plotter

python ../main.py -U $EXTERNAL_POTENTIAL -ph $PH
