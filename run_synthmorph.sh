#!/bin/bash

mkdir -p outputs

# Run synthmorph
echo "Running synthmorph"
for mag in `seq 0 5 20`; do
    echo "Magnitude: ${mag}"
    for i in `seq 0 9` ; do
        python3 ./scripts/tf/register.py --moving inputs/noised_image_magnitude_${mag}_${i}.npz  --fixed data/atlas.npz --moved outputs/moved_all_${mag}_${i}.nii.gz --model data/brain_3d.h5
        python3 ./scripts/tf/register.py --moving inputs/noised_image_one_voxel_magnitude_${mag}_${i}.npz  --fixed data/atlas.npz --moved outputs/moved_one_${mag}_${i}.nii.gz --model data/brain_3d.h5
    done
done
