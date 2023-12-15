import nibabel
import numpy as np
import nilearn.plotting
import argparse


def load_file(filename):
    if filename.endswith(".nii.gz"):
        img = nibabel.load(filename)
        return img
    if filename.endswith(".npy"):
        img = np.load(filename)
        img = nibabel.Nifti1Image(img, np.eye(4))
        return img
    if filename.endswith(".npz"):
        img = np.load(filename)
        img = nibabel.Nifti1Image(img["vol"], np.eye(4))
        return img


def view_nii(img, metrics, title, coords):
    if metrics == "sig":
        cmap = "RdYlGn"
        vmin = 0
        vmax = 24
    elif metrics == "intensity":
        cmap = "Greys_r"
        vmin = None
        vmax = None
    else:
        raise ValueError("Unknown metrics: {}".format(metrics))

    if coords:
        coords = tuple(map(int, coords.split(",")))

    data = img.get_fdata()
    data = np.where(data < 0, 0, data)
    img = nibabel.Nifti1Image(data, np.eye(4))

    view = nilearn.plotting.view_img(
        img,
        black_bg=True,
        bg_img=None,
        symmetric_cmap=False,
        cmap=cmap,
        colorbar=True,
        vmin=vmin,
        vmax=vmax,
        title=title,
        threshold=None,
        cut_coords=coords,
    )

    view.open_in_browser()


def save_image(img, filename):
    nibabel.save(img, filename)


def print_info(img):
    data = img.get_fdata()
    print("shape: {}".format(data.shape))
    print("min: {}".format(data.min()))
    print("max: {}".format(data.max()))
    print("mean: {}".format(data.mean()))
    print("std: {}".format(data.std()))
    print("dtype: {}".format(data.dtype))


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input",
        type=str,
        required=True,
        help="Path to the input image",
    )
    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="Path to the output image",
    )
    parser.add_argument(
        "--metrics",
        type=str,
        required=True,
        help="Metrics to visualize",
    )
    parser.add_argument("--coords", type=str, default=None, help="Coordinates")
    parser.add_argument("--title", type=str, default=None, help="Title of the plot")
    return parser.parse_args()


def main():
    args = parse_args()
    img = load_file(args.input)
    print_info(img)
    view_nii(img, args.metrics, args.title, args.coords)
    if args.output:
        save_image(img, args.output)


if __name__ == "__main__":
    main()
