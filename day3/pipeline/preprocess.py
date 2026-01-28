# preprocess.py
# Responsibility:
# - Resize and normalize camera frames
# - Return model-ready float32 image

import cv2
import numpy as np


def preprocess(frame, size=(224, 224)):
    """
    Resize and normalize image for model input.

    Constraints:
    - Use float32
    - Normalize to [0, 1]
    - Resize FIRST, then normalize
    - Keep dimensions consistent (HxWxC → CHW if needed)

    Think:
    - Why float32 and not uint8?
    - Why resize before normalization?
    """

    # TODO 1: Resize the frame to 'size' (e.g., 224x224)
    # Use OpenCV resize
    frame = cv2.resize(frame, size)

    # TODO 2: Convert to float32
    frame = frame.astype(np.float32)

    # TODO 3: Normalize pixels to range [0, 1]
    frame = frame / 255.0
    
    frame = np.transpose(frame, (2, 0,1))

    return frame  # final processed image
