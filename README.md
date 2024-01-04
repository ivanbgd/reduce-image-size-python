# Reduce Image Size

## Description
Reduces size of images in a folder (and optionally sub-folders, recursively).

This is useful for archiving of photos, for example, as they look the same on a display even with a reduced file size.  
This application reduces file sizes of images in bulk.

By default, keeps the original images and creates copies with reduced file size.

By default, copies the entire folder tree, with all sub-folders that exist in the source tree.  
The target folder tree will be created automatically, and the new reduced-size images will be copied properly to their respective paths.  
It is only required to provide the root target folder, and it will also be created if it doesn't exist.  
Non-supported files will simply be copied to the destination.

The destination folder can be the same as the source folder, in which case the original images will be **overwritten**, and not retained.  
Other, non-supported files, will be retained.

If there is enough disk space, it is advised to specify a different destination folder than the source folder,
so that the original images can be retained and the newly-created reduced-size images can be inspected for quality.  
A user can experiment with the `resize` and the `quality` arguments.  
Also, the user can go only one level deep and not recursively, or simply experiment on a copy of an image folder.  
If satisfied with the result, original images can be deleted afterwards easily to save disk and/or cloud space.

## Options
- Look into subdirectories recursively (process the entire tree); recommended: `-r`, `--recursive`
- Reduce both image dimensions by half: `--resize`
- JPEG quality, on a scale from 0 (worst) to 95 (best); the default is 75; ignored in case of PNGs: `--quality [QUALITY]`
- A minimum file size for which a user would like to perform file size reduction: `-s {s,m,l,S,M,L}`, `--size {s,m,l,S,M,L}`
  - S = 100 kB, M = 500 kB, L = 1 MB
  - Files that are smaller than the designated size will simply be copied to the destination folder.

## Notes
- Developed in Python 3.12.0.
- Tested on an x86-64 CPU on Windows 11.
- Tested with JPEGs and PNGs.
- Might work with other image formats, too, but this hasn't been tested. Use at own risk, and work on a copy, as advised above.
- Other OSes haven't been tested, but should work.

## Running the Application
Go to the repository directory.

Create & activate virtual environment and install requirements:  
```commandline
python -m venv venv
python -m pip install --upgrade pip
pip install -r requirements.txt
```
That only needs to be done once.

If inside the repository directory, activate the virtual environment:  
- Windows: `venv\Scripts\activate`  
- Linux & macOS: `source venv/bin/activate`

and run the program as:  
- Windows: `python src\reduce.py <source_folder> <destination_folder> [options]`  
- Linux & macOS: `python src/reduce.py <source_folder> <destination_folder> [options]`

Or, provide full path to the program.

Paths to the source and destination folders can be absolute or relative.
