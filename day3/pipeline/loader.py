# loader.py
# Responsibility:
# 1. Discover image files
# 2. Return file paths (NOT images)
# 3. Read image ONLY when explicitly asked

import os
import cv2


def load_image_paths(folder):
    """
    Given a folder path, return a list of image file paths.

    Constraints:
    - Do NOT read images here
    - Do NOT store image data in memory
    - Only work with file paths

    Think:
    - Why is this better for edge devices?
    """

    image_paths = []

    # TODO:
    # 1. Iterate through files in the folder
    # 2. Check for valid image extensions (.jpg, .png)
    # 3. Construct full file paths
    # 4. Append to image_paths list
    valid_exts = (".jpg", ".jpeg", ".png")

    for filename in os.listdir(folder):
        if filename.lower().endswith(valid_exts):
            full_path = os.path.join(folder, filename)
            if os.path.isfile(full_path):
                image_paths.append(full_path)

    return image_paths


def read_image(path):
    """
    Read a single image from disk.

    Constraints:
    - Accept ONE file path
    - Return ONE image
    - No resizing / preprocessing here

    Think:
    - Why should reading be separate from preprocessing?
    """

    # TODO:
    # 1. Use OpenCV to read the image
    # 2. Handle failure cases (image not found / corrupted)
    image = cv2.imread(path)

    if image is None:
        raise FileNotFoundError(f"Could not read image: {path}")

    return image