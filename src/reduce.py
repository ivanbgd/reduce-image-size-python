import argparse
import datetime
import timeit
from pathlib import Path

from PIL import Image

QUALITY = 75


def different_paths(src_dir: Path, dst_dir: Path, recursive: bool, resize: bool, quality: int) -> None:
    src_paths = src_dir.glob("*") if not recursive else src_dir.glob("**/*")

    for src_path in src_paths:
        try:
            with Image.open(src_path) as image:
                if resize:
                    image_size = image.size
                    # Downsize the image with the LANCZOS filter (gives the highest quality).
                    new_size = (image_size[0] // 2, image_size[1] // 2)
                    image = image.resize(new_size, Image.Resampling.LANCZOS)

                dst_path: Path = dst_dir / src_path.relative_to(src_dir)
                dst_path.parent.mkdir(parents=True, exist_ok=True)

                # The argument `optimize` is used for both JPEGs and PNGs.
                # The argument `quality` is used for JPEGs, and simply ignored in case of PNGs.
                image.save(dst_path, optimize=True, quality=quality)
                print(f"Resized \"{src_path}\" to \"{dst_path}\".", flush=True)
        except Exception as e:
            print(e)


def same_paths(src_dir: Path, recursive: bool, resize: bool, quality: int) -> None:
    src_paths = src_dir.glob("*") if not recursive else src_dir.glob("**/*")

    for src_path in src_paths:
        try:
            with Image.open(src_path) as image:
                if resize:
                    image_size = image.size
                    new_size = (image_size[0] // 2, image_size[1] // 2)
                    image = image.resize(new_size, Image.Resampling.LANCZOS)

                image.save(src_path, optimize=True, quality=quality)
                print(f"Resized \"{src_path}\".", flush=True)
        except Exception as e:
            print(e)


def process_images(src_dir: Path, dst_dir: Path, recursive: bool, resize: bool, quality: int) -> None:
    print(f"JPEG quality = {quality}\n", flush=True)

    if src_dir != dst_dir:
        different_paths(src_dir, dst_dir, recursive, resize, quality)
    else:
        same_paths(src_dir, recursive, resize, quality)


def main() -> None:
    start = timeit.default_timer()

    parser = argparse.ArgumentParser(
        prog="python src\\reduce.py",
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
        help="path to destination folder for reduced-size copies of original images; "
             "can be the same as source, in which case source images are overwritten"
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
    parser.add_argument(
        "--quality",
        type=int,
        nargs="?",
        default=QUALITY,
        const=QUALITY,
        help=f"JPEG quality, on a scale from 0 (worst) to 95 (best); "
             f"the default is {QUALITY}; ignored in case of PNGs"
    )

    args = parser.parse_args()
    src_dir: Path = Path(args.src_dir)
    dst_dir: Path = Path(args.dst_dir)
    recursive: bool = args.recursive
    resize: bool = args.resize
    quality: int = args.quality

    try:
        dst_dir.mkdir(parents=True, exist_ok=True)
    except FileExistsError:
        print(f"\"{dst_dir}\" exists and is a file! Provide a proper target directory.")
        return

    process_images(src_dir, dst_dir, recursive, resize, quality)

    end = timeit.default_timer()
    diff = end - start
    print(f"\nTook {datetime.timedelta(seconds=diff)} or {diff:.3f} s to complete.")


if __name__ == "__main__":
    main()
