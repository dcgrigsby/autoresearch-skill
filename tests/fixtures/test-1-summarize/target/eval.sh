#!/bin/bash
# Runs the scorer and prints a single number (pass rate 0.0–1.0).
# Higher is better.
set -e
python3 "$(dirname "$0")/scorer.py"
