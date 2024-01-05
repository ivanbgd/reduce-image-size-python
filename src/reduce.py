import argparse
import datetime
import shutil
import timeit
from pathlib import Path

from PIL import Image

from constants import QUALITY, Size


def different_paths(src_dir: Path, dst_dir: Path, recursive: bool, resize: bool, quality: int, size: Size) -> None:
    src_paths = src_dir.glob("*") if not recursive else src_dir.glob("**/*")

    for src_path in src_paths:
        if src_path.is_file():
            # This `mkdir` shouldn't be able to raise (at least not in Python <= 3.12.0),
            # and the same goes for `relative_to` in this case, so they are not wrapped in try-except.
            dst_path: Path = dst_dir / src_path.relative_to(src_dir)
            dst_path.parent.mkdir(parents=True, exist_ok=True)

            if src_path.stat().st_size >= size:
                try:
                    # We could add the `formats` argument to restrict the set of formats checked,
                    # but we don't want to restrict it.
                    with Image.open(src_path) as image:
                        if resize:
                            image_size = image.size
                            # Downsize the image with the LANCZOS filter (gives the highest quality).
                            new_size = (image_size[0] // 2, image_size[1] // 2)
                            image = image.resize(new_size, Image.Resampling.LANCZOS)

                        # The argument `optimize` is used for both JPEGs and PNGs.
                        # The argument `quality` is used for JPEGs, and simply ignored in case of PNGs.
                        image.save(dst_path, optimize=True, quality=quality)
                        print(f"Reduced \"{src_path}\" to \"{dst_path}\".", flush=True)
                except Exception as e:
                    print(e)
                    # Whatever the reason for failure may be, let's just copy the file to the destination.
                    # Perhaps it wasn't an image file to begin with, so PIL was not able to process it.
                    shutil.copy2(src_path, dst_path)
                    print(f"Copied \"{src_path}\" to \"{dst_path}\".", flush=True)
            else:
                # Simply copy the file, whether it's an image or not.
                shutil.copy2(src_path, dst_path)
                print(f"Copied \"{src_path}\" to \"{dst_path}\".", flush=True)


def same_paths(src_dir: Path, recursive: bool, resize: bool, quality: int, size: Size) -> None:
    src_paths = src_dir.glob("*") if not recursive else src_dir.glob("**/*")

    for src_path in src_paths:
        if src_path.is_file():
            if src_path.stat().st_size >= size:
                try:
                    with Image.open(src_path) as image:
                        if resize:
                            image_size = image.size
                            new_size = (image_size[0] // 2, image_size[1] // 2)
                            image = image.resize(new_size, Image.Resampling.LANCZOS)

                        image.save(src_path, optimize=True, quality=quality)
                        print(f"Reduced \"{src_path}\".", flush=True)
                except Exception as e:
                    print(e)
                    print(f"Skipped \"{src_path}\".", flush=True)
            else:
                print(f"Skipped \"{src_path}\".", flush=True)


def process_images(src_dir: Path, dst_dir: Path, recursive: bool, resize: bool, quality: int, size: Size) -> None:
    if src_dir != dst_dir:
        different_paths(src_dir, dst_dir, recursive, resize, quality, size)
    else:
        same_paths(src_dir, recursive, resize, quality, size)


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
    parser.add_argument(
        "-s", "--size",
        type=str,
        nargs=1,
        choices=["s", "m", "l", "S", "M", "L"],
        help="A minimum file size for which to perform file size reduction; "
             "S = 100 kB, M = 500 kB, L = 1 MB"
    )

    args = parser.parse_args()
    src_dir: Path = Path(args.src_dir)
    dst_dir: Path = Path(args.dst_dir)
    recursive: bool = args.recursive
    resize: bool = args.resize
    quality: int = args.quality

    match args.size:
        case ["s"] | ["S"]: size = Size.S
        case ["m"] | ["M"]: size = Size.M
        case ["l"] | ["L"]: size = Size.L
        case _: size = Size.DEFAULT

    try:
        dst_dir.mkdir(parents=True, exist_ok=True)
    except FileExistsError:
        print(f"\"{dst_dir}\" exists and is a file! Provide a proper target directory.")
        return

    print(f"Process recursively: {recursive}")
    print(f"Reduce image dimensions: {resize}")
    print(f"Minimum image file size for processing is {size} bytes.")
    print(f"JPEG quality = {quality}\n", flush=True)

    process_images(src_dir, dst_dir, recursive, resize, quality, size)

    end = timeit.default_timer()
    diff = end - start
    print(f"\nTook {datetime.timedelta(seconds=diff)} or {diff:.3f} s to complete.")


if __name__ == "__main__":
    main()
