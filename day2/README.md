# Day 2 — Basic Image Pipeline with FPS Monitoring

## Overview
This activity implements a **lightweight edge-style image processing pipeline** focused on **efficient data loading, preprocessing, batching, and performance monitoring**.

The goal of Day 2 is to establish a **baseline pipeline** with measurable **FPS and memory usage**, which later stages build upon.

This design is suitable for **Edge AI devices (e.g., NVIDIA Jetson Nano)** where memory and throughput are critical.

---

## Folder Structure
```
day2/
├── pipeline/
│   ├── loader.py       # Image path discovery & validation
│   ├── preprocess.py  # Image preprocessing
│   └── stream.py      # Batched image streaming
├── utils/
│   └── monitor.py     # FPS & system memory monitoring
├── main.py            # Pipeline orchestration
└── setup.sh           # Environment setup
```

---

## Pipeline Flow
```
Image Directory
      ↓
loader.py  → validates image paths
      ↓
stream.py  → batches images from disk
      ↓
preprocess.py → resize + normalize
      ↓
main.py → FPS & memory monitoring
```

---

## Module Details

### `pipeline/loader.py`
- Scans the input directory for valid image files
- Supported formats:
  - `.jpg`, `.jpeg`, `.png`, `.bmp`
- Only image **paths** are loaded initially (lazy loading)
- Prevents unnecessary memory usage

---

### `pipeline/preprocess.py`
Handles image normalization before inference.

Operations:
```python
img = cv2.resize(img, (224, 224))
img = img.astype(np.float32) / 255.0
```

Why this matters:
- Early resizing reduces compute cost
- Normalization prepares data for ML models
- Matches common CNN input requirements

---

### `pipeline/stream.py`
- Streams images from disk
- Supports configurable **batch size**
- Uses generators (`yield`) to avoid loading all images into memory

This simulates **real-world data pipelines** used in edge inference systems.

---

### `utils/monitor.py`
Provides real-time system metrics:
- **FPSCounter**
  - Tracks total FPS across batches
  - Updates based on actual number of images processed
- **system_stats**
  - Reports memory usage (MB)

This makes performance **visible and measurable**, not assumed.

---

## Main Execution (`main.py`)

Key logic:
- Loads image paths
- Streams images in **batches of 4**
- Simulates processing delay
- Tracks FPS and memory usage per batch

Example output:
```
Batch Size: 4 | Total FPS: XX.XX | Mem(MB): XXX.XX
```

This establishes a **baseline performance reference** for later stages.

---

## Why This Design
- **Modular**: Easy to extend with inference stages
- **Memory-efficient**: No full dataset loading
- **Performance-aware**: FPS and memory are tracked explicitly
- **Edge-ready**: Suitable for Jetson-class devices

---

## How to Run
1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the pipeline:
```bash
python3 main.py
```

---

## Outcome
- Functional real-time image pipeline
- Measured FPS and memory usage
- Clean baseline for adding inference and deployment optimizations
