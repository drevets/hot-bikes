#!/usr/bin/env bash

source activate hot-bikes
python -m unittest discover --pattern="*_tests.py"