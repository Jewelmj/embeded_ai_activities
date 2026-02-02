import cv2
import numpy as np

def preprocess_image(img, size=(224, 224)):
    # TODO 1: Resize first to reduce memory footprint for subsequent steps
    img = cv2.resize(img, size)
    
    # TODO 2 & 3: Convert to float32 and normalize [0, 1] in-place
    # Using float32 instead of float64 saves 50% memory per pixel
    img = img.astype(np.float32) / 255.0
    return img