#!/bin/bash
mkdir -p inputs

# Generate input noised image
echo "Generating input noised image"
python3 add_noise.py --input data/subj1.npz --output inputs --n 10
