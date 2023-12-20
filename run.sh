#!/bin/bash

mkdir -p inputs outputs stats/sig/{inputs,outputs}

# Generate input noised image
echo "Generating input noised image"
python3 add_noise.py --input data/subj1.npz --output inputs --n 10

# Compute sig digits on inputs
echo "Computing sig digits on inputs"
for mag in `seq 0 5 20`; do
    echo "Magnitude: ${mag}"
    python3 compute_sig.py --input "inputs/noised_image_magnitude_${mag}_*.npz" --output-directory stats/sig/inputs/ --output sig_input_all_${mag}.nii.gz
    python3 compute_sig.py --input "inputs/noised_image_one_voxel_magnitude_${mag}_*.npz" --output-directory stats/sig/inputs/ --output sig_input_one_${mag}.nii.gz
done

# Run synthmorph
echo "Running synthmorph"
for mag in `seq 0 5 20`; do
    echo "Magnitude: ${mag}"
    for i in `seq 0 9` ; do
        python3 ./scripts/tf/register.py --moving inputs/noised_image_magnitude_${mag}_${i}.npz  --fixed data/atlas.npz --moved outputs/moved_all_${mag}_${i}.nii.gz --model data/brain_3d.h5
        python3 ./scripts/tf/register.py --moving inputs/noised_image_one_voxel_magnitude_${mag}_${i}.npz  --fixed data/atlas.npz --moved outputs/moved_one_${mag}_${i}.nii.gz --model data/brain_3d.h5
    done
done

# Compute sig digits on outputs
echo "Computing sig digits on outputs"
for mag in `seq 0 5 20`; do
    echo "Magnitude: ${mag}"
    python3 compute_sig.py --input "outputs/moved_all_${mag}_*.nii.gz" --output-directory stats/sig/outputs/ --output sig_output_all_${mag}.nii.gz
    python3 compute_sig.py --input "outputs/moved_one_${mag}_*.nii.gz" --output-directory stats/sig/outputs/ --output sig_output_one_${mag}.nii.gz
done