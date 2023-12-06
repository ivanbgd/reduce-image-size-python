import argparse
from pathlib import Path

from PIL import Image

QUALITY = 75


def process_images(src_dir: Path, dst_dir: Path, recursive: bool, resize: bool) -> None:
    src_paths = src_dir.glob("*") if not recursive else src_dir.glob("**/*")

    for src_path in src_paths:
        # print(f"Source: {src_path}") ###
        try:
            with Image.open(src_path) as image:
                if resize:
                    image_size = image.size
                    # Downsize the image with the LANCZOS filter (gives the highest quality).
                    new_size = (image_size[0] // 2, image_size[1] // 2)
                    image = image.resize(new_size, Image.Resampling.LANCZOS)

                dst_path: Path = dst_dir / src_path.relative_to(src_dir)
                # print(f"Dest: {dst_path}")  ###
                # The argument `quality` is used for JPEGs, and simply ignored in case of PNGs.
                # image.save(dst_path, optimize=True, quality=QUALITY)
        except Exception as e:
            print(e)


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="Reduce Image Size",
        description="Reduces size of images in a folder (and optionally sub-folders)"
    )

    parser.add_argument(
        "src_dir",
        type=str,
        help="path to source folder with original images"
    )
    parser.add_argument(
        "dst_dir",
        type=str,
        help="path to destination folder for reduced-size copies of original images"
    )
    parser.add_argument(
        "-r", "--recursive",
        action="store_true",
        help="look recursively in sub-folders"
    )
    parser.add_argument(
        "--resize",
        action="store_true",
        help="reduce both image dimensions by half"
    )

    args = parser.parse_args()
    src_dir: Path = Path(args.src_dir)
    dst_dir: Path = Path(args.dst_dir)
    recursive: bool = args.recursive
    resize: bool = args.resize

    try:
        dst_dir.mkdir(parents=True, exist_ok=True)
    except FileExistsError:
        print(f"\"{dst_dir}\" exists and is a file! Provide a proper target directory.")
        return

    process_images(src_dir, dst_dir, recursive, resize)


if __name__ == "__main__":
    main()
