#!/bin/bash

# Define external potential and pH
EXTERNAL_POTENTIAL=0
PH=14

# Call the calculator
python ../main.py -U $EXTERNAL_POTENTIAL -ph $PH
