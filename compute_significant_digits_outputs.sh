#!/bin/bash

mkdir -p stats/sig/outputs


# Compute sig digits on outputs
echo "Computing sig digits on outputs"
for mag in `seq 0 5 20`; do
    echo "Magnitude: ${mag}"
    python3 compute_sig.py --input "outputs/moved_all_${mag}_*.nii.gz" --output-directory stats/sig/outputs/ --output sig_output_all_${mag}.nii.gz
    python3 compute_sig.py --input "outputs/moved_one_${mag}_*.nii.gz" --output-directory stats/sig/outputs/ --output sig_output_one_${mag}.nii.gz
done