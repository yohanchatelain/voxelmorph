from calendar import c
import nibabel
import numpy as np
import os


def load_image(filename):
    img = np.load(filename)
    return img


def add_noise_all(img, magnitude):
    data = img["vol"]
    eps = np.finfo(data.dtype).eps * 2**magnitude
    data *= np.random.choice([(1 - eps), (1 + eps)], size=data.shape)
    new_img = {}
    new_img["vol"] = data
    new_img["seg"] = img["seg"]
    return new_img


def add_noise_one_voxel(img, magnitude):
    data = img["vol"]
    eps = np.finfo(data.dtype).eps * 2**magnitude
    pos = np.array(data.shape) // 2
    data[tuple(pos)] *= np.random.choice([(1 - eps), (1 + eps)], size=1)[0]
    new_img = {}
    new_img["vol"] = data
    new_img["seg"] = img["seg"]
    return new_img


def save_image(img, filename):
    np.savez(filename, vol=img["vol"], seg=img["seg"])


def create_noised_image(output_directory, img, n, noised_type, magnitude=0):
    if noised_type == "all":
        add_noise = add_noise_all
        suffix = "noised_image" + "_magnitude_" + str(magnitude)
    elif noised_type == "one":
        add_noise = add_noise_one_voxel
        suffix = "noised_image_one_voxel" + "_magnitude_" + str(magnitude)
    else:
        raise ValueError("Unknown noised type: {}".format(noised_type))

    for i in range(n):
        img = add_noise(img, magnitude)
        output_path = os.path.join(output_directory, suffix + "_" + str(i))
        save_image(img, output_path)


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
        "--output",
        type=str,
        required=True,
        help="Path to the output directory",
    )
    parser.add_argument(
        "--n",
        type=int,
        required=True,
        help="Number of noised images to generate",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    img = load_image(args.input)
    if args.output is None:
        output_directory = os.path.dirname(args.input)
    elif not os.path.exists(args.output):
        os.makedirs(args.output)
        output_directory = args.output
    elif os.path.isdir(args.output):
        output_directory = args.output
    else:
        output_directory = "."

    create_noised_image(output_directory, img, args.n, "all", 0)
    create_noised_image(output_directory, img, args.n, "one", 0)

    create_noised_image(output_directory, img, args.n, "all", 5)
    create_noised_image(output_directory, img, args.n, "one", 5)

    create_noised_image(output_directory, img, args.n, "all", 10)
    create_noised_image(output_directory, img, args.n, "one", 10)

    create_noised_image(output_directory, img, args.n, "all", 15)
    create_noised_image(output_directory, img, args.n, "one", 15)

    create_noised_image(output_directory, img, args.n, "all", 20)
    create_noised_image(output_directory, img, args.n, "one", 20)


if __name__ == "__main__":
    main()
