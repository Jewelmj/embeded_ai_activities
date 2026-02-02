import os
import cv2

def load_image_paths(folder):
    image_paths = []
    valid_extensions = ('.jpg', '.jpeg', '.png', '.bmp')
    # 1. Iterate through files; 2. Check extensions; 3. Construct full paths
    if os.path.exists(folder):
        for file in os.listdir(folder):
            if file.lower().endswith(valid_extensions):
                image_paths.append(os.path.join(folder, file))
    return image_paths

def read_image(path):
    # 1. Use OpenCV to read; 2. Handle failure cases
    image = cv2.imread(path)
    if image is None:
        print(f"Warning: Could not read image at {path}")
    return image