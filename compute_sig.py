from matplotlib import axis
import significantdigits as sd
import numpy as np
import os
import nibabel
import glob


def load_image(filename):
    if filename.endswith(".nii.gz"):
        img = nibabel.load(filename).get_fdata()
        return img
    if filename.endswith(".npy"):
        img = np.load(filename)
        return img
    if filename.endswith(".npz"):
        img = np.load(filename)
        return img["vol"]


def compute_sig(data):
    mask = np.std(data, axis=0) > 0
    sig = sd.significant_digits(data, reference=data.mean(axis=0), dtype=np.float32)
    return sig, mask


def get_files(regexp):
    return glob.glob(regexp)


def load_images(regexp):
    return np.array([load_image(f) for f in get_files(regexp)])


def save_image(img, dir, filename):
    if not filename.endswith(".nii.gz"):
        filename += ".nii.gz"
    path = os.path.join(dir, filename)
    niimg = nibabel.Nifti1Image(img, np.eye(4))
    nibabel.save(niimg, path)


def save_mask(img, dir, filename):
    if not filename.endswith(".nii.gz"):
        filename += ".nii.gz"
    filename = filename.replace(".nii.gz", "_mask.nii.gz")
    path = os.path.join(dir, filename)
    niimg = nibabel.Nifti1Image(img, np.eye(4))
    nibabel.save(niimg, path)


def parse_args():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input",
        type=str,
        required=True,
        help="Path to the input image",
    )
    parser.add_argument(
        "--output-directory",
        type=str,
        default=".",
        help="Path to the output directory",
    )
    parser.add_argument(
        "--output",
        type=str,
        required=True,
        help="Output filename for the significant digits image",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    img = load_images(args.input)
    sig, mask = compute_sig(img)

    dirname = os.path.dirname(args.output)
    if dirname != "" and not os.path.exists(dirname):
        os.makedirs(dirname)

    save_image(sig, args.output_dir, args.output)
    save_mask(mask, args.output_dir, args.output)


if __name__ == "__main__":
    main()
