#!/bin/bash

# --- Global Configuration & Error Handling ---
set -e  # Exit on any error
trap 'echo "❌ Error occurred at line $LINENO. Check logs."; exit 1' ERR

echo "🚀 Initializing Edge AI Data Pipeline for Jetson Nano..."

# --- Step 1: Directory Structure ---
# Rule 1: Never load full dataset. We maintain a strict folder structure.
mkdir -p data/images pipeline utils

# --- Step 2: Component Creation (Python Files) ---

# 2.1 Loader Component (Lazy Discovery)
cat <<EOT > pipeline/loader.py
import os
import cv2

def load_image_paths(folder):
    """Rule 1: Return paths only, NOT images"""
    valid_extensions = ('.jpg', '.png', '.jpeg')
    if not os.path.exists(folder):
        return []
    return [os.path.join(folder, f) for f in os.listdir(folder) if f.lower().endswith(valid_extensions)]

def read_image(path):
    """Separate reading from processing to keep modularity."""
    img = cv2.imread(path)
    return img if img is not None else None
EOT

# 2.2 Preprocess Component (Edge Optimization)
cat <<EOT > pipeline/preprocess.py
import cv2
import numpy as np

def preprocess_image(img, size=(224, 224)):
    """
    Rule 2: Resize as early as possible.
    Rule 3: Normalize once.
    Experiment 3: Use float32 to avoid FPS drops.
    """
    # Resize FIRST to reduce memory footprint immediately
    img = cv2.resize(img, size)
    # Convert to float32 (NOT float64) to maintain speed
    img = img.astype(np.float32) / 255.0
    return img
EOT

# 2.3 Stream Component (Lazy Generators & Batching)
cat <<EOT > pipeline/stream.py
from pipeline.loader import read_image
from pipeline.preprocess import preprocess_image

def image_stream(image_paths, batch_size=4):
    """
    Rule 4: Use generators (yield).
    Experiment 4: Add batching of 4 images.
    """
    batch = []
    for path in image_paths:
        img = read_image(path)
        if img is not None:
            processed = preprocess_image(img)
            batch.append(processed)
        
        if len(batch) == batch_size:
            yield batch
            batch = []
    if batch:
        yield batch
EOT

# 2.4 Monitor Component (Resource Tracking)
cat <<EOT > utils/monitor.py
import psutil
import time

def system_stats():
    """Rule 5: Measure memory usage."""
    return psutil.virtual_memory().used / (1024 * 1024)

class FPSCounter:
    def __init__(self):
        self.start = None
        self.frames = 0
    def start_timer(self):
        self.start = time.time()
    def update(self, count=1):
        self.frames += count
        elapsed = time.time() - self.start
        return self.frames / elapsed if elapsed > 0 else 0.0
EOT

# 2.5 Main Execution Script
cat <<EOT > main.py
from pipeline.loader import load_image_paths
from pipeline.stream import image_stream
from utils.monitor import system_stats, FPSCounter
import time

IMAGE_DIR = "data/images"
paths = load_image_paths(IMAGE_DIR)

if not paths:
    print("⚠️ No images found! Adding samples...")
    # This block will be triggered by the .sh script below
else:
    # Experiment 4: Batching of 4
    stream = image_stream(paths, batch_size=4)
    fps = FPSCounter()
    fps.start_timer()

    print("📊 Pipeline Running (Batch Size: 4)")
    for batch in stream:
        time.sleep(0.1)  # Simulate inference latency
        fps_val = fps.update(count=len(batch))
        mem = system_stats()
        print(f"Batch Processed | Total FPS: {fps_val:.2f} | Mem(MB): {mem:.2f}")
EOT

# --- Step 3: Dependency Installation ---
echo "📦 Installing Requirements for Jetson..."
pip3 install opencv-python-headless psutil numpy --quiet

# --- Step 4: Data Acquisition ---
if [ -z "$(ls -A data/images)" ]; then
    echo "📥 Downloading Test Images..."
    wget -q -P data/images https://raw.githubusercontent.com/opencv/opencv/master/samples/data/lena.jpg
    wget -q -P data/images https://raw.githubusercontent.com/opencv/opencv/master/samples/data/baboon.jpg
fi

# --- Step 5: Execution & Observation ---
echo "🏁 Starting Pipeline Execution..."
python3 main.py

echo "✅ All steps completed successfully."