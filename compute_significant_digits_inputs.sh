#!/bin/bash

mkdir -p stats/sig/inputs

# Compute sig digits on inputs
echo "Computing sig digits on inputs"
for mag in `seq 0 5 20`; do
    echo "Magnitude: ${mag}"
    python3 compute_sig.py --input "inputs/noised_image_magnitude_${mag}_*.npz" --output-directory stats/sig/inputs/ --output sig_input_all_${mag}.nii.gz
    python3 compute_sig.py --input "inputs/noised_image_one_voxel_magnitude_${mag}_*.npz" --output-directory stats/sig/inputs/ --output sig_input_one_${mag}.nii.gz
done
