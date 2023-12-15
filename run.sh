#!/bin/bash

# Generate input noised image
echo "Generating input noised image"
python3 add_noise.py --input data/subj1.npz --output noised_image --n 10

# Compute sig digits on inputs
echo "Computing sig digits on inputs"
for mag in `seq 0 5 20`; do
    echo "Magnitude: ${mag}"
    python3 compute_sig.py --input "noised_image/noised_image_magnitude_${mag}_*.npz" --output sig_input_all_${mag}.nii.gz
    python3 compute_sig.py --input "noised_image/noised_image_one_voxel_magnitude_${mag}_*.npz" --output sig_input_one_${mag}.nii.gz
done

# parallel --header :  "python3 compute_sig.py --input 'noised_image/noised_image_magnitude_{mag}_*.npz' --output sig_input_all_{mag}.nii.gz" ::: mag `seq 0 5 20`
# parallel --header :  "python3 compute_sig.py --input 'noised_image/noised_image_one_voxel_magnitude_{mag}_*.npz' --output sig_input_one_{mag}.nii.gz" ::: mag `seq 0 5 20`

# Run synthmorph
echo "Running synthmorph"
for mag in `seq 0 5 20`; do
    echo "Magnitude: ${mag}"
    for i in `seq 0 9` ; do
        python3 ./scripts/tf/register.py --moving noised_image/noised_image_magnitude_${mag}_${i}.npz  --fixed data/atlas.npz --moved moved_all_${mag}_${i}.nii.gz --model data/brain_3d.h5
        python3 ./scripts/tf/register.py --moving noised_image/noised_image_one_voxel_magnitude_${mag}_${i}.npz  --fixed data/atlas.npz --moved moved_one_${mag}_${i}.nii.gz --model data/brain_3d.h5
    done
done

# parallel --header : python3 ./scripts/tf/register.py --moving noised_image/noised_image_magnitude_{mag}_{i}.npz  --fixed data/atlas.npz --moved moved_all_{mag}_{i}.nii.gz --model data/brain_3d.h5  ::: i `seq 0 9` ::: mag `seq 0 5 20`
# parallel --header : python3 ./scripts/tf/register.py --moving noised_image/noised_image_one_voxel_magnitude_{mag}_{i}.npz  --fixed data/atlas.npz --moved moved_one_{mag}_{i}.nii.gz --model data/brain_3d.h5  ::: i `seq 0 9` ::: mag `seq 0 5 20`

# Compute sig digits on outputs
echo "Computing sig digits on outputs"
for mag in `seq 0 5 20`; do
    echo "Magnitude: ${mag}"
    python3 compute_sig.py --input "moved_all_${mag}_*.nii.gz" --output outputs/sig_output_all_${mag}.nii.gz
    python3 compute_sig.py --input "moved_one_${mag}_*.nii.gz" --output outputs/sig_output_one_${mag}.nii.gz
done

# parallel --header :  python3 compute_sig.py --input 'outputs/moved_all_{mag}_*.npz' --output outputs/sig_output_all_{mag}.nii.gz ::: mag 0 5 20
# parallel --header :  python3 compute_sig.py --input 'outputs/moved_one_voxels_{mag}_*.npz' --output outputs/sig_output_one_{mag}.nii.gz ::: mag 0 5 20
