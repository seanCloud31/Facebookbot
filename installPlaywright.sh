#!/bin/bash

# Install Playwright via pip
pip install playwright

# Install Playwright dependencies
playwright install

# Install NumPy via pip
pip install numpy

# Install Playwright dependencies (again, just in case)
playwright install-deps

# Run the Python script seanCloud.py
python seanCloud.py