from PIL import Image

QUALITY = 75

IMAGE = "C:/Slika/pngwing.com"
EXT = "jpg"
EXT = "png"

resize = False  # todo make it cli arg

# TODO loop through all jpg, jpeg, png files; use .lower() on file names first
# It's good enough to loop over ALL files, because we are guarding against errors below.
# See https://pillow.readthedocs.io/en/stable/handbook/tutorial.html#batch-processing

image_path = f"{IMAGE}.{EXT}" ###

try:
    # with Image.open(f"{IMAGE}.{EXT}") as image:###
    with Image.open(image_path) as image:
        if resize:
            # TODO: Make resizing optional.
            image_size = image.size
            # Downsize the image with the LANCZOS filter (gives the highest quality)
            new_size = (image_size[0] // 2, image_size[1] // 2)
            image = image.resize(new_size, Image.Resampling.LANCZOS)

        # image.save(f"{IMAGE}_resized_resampled_opt.{EXT}", optimize=True, quality=QUALITY)###

        # Save in-place - overwrite original image
        image.save(image_path, optimize=True, quality=QUALITY)
except Exception as e:
    print(e)
