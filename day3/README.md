# Day 3 — Camera-Based Pipeline with Frame Sampling & Dummy Inference

## Overview
Day 3 extends the Day 2 image pipeline into a **live camera-based edge pipeline**.  
This stage introduces **frame sampling, preprocessing for model-ready tensors, simulated inference latency, and enhanced performance monitoring**.

The objective is to understand **how inference latency impacts FPS** and how **intentional frame dropping** is used in real-time systems to maintain stability on edge devices.

---

## Folder Structure
```
day3/
├── camera/
│   └── webcam.py        # Webcam capture & release
├── inference/
│   └── dummy_inference.py  # Simulated inference delay
├── pipeline/
│   ├── loader.py        # (Optional) data helpers
│   ├── preprocess.py   # Frame preprocessing
│   └── sampler.py      # FPS-based frame sampler
├── utils/
│   └── metrics.py      # FPS & memory monitoring utilities
├── main.py              # Full pipeline orchestration
└── README.md
```

---

## Pipeline Flow
```
Webcam
  ↓
FrameSampler (FPS control)
  ↓
Preprocess (tensor formatting)
  ↓
Dummy Inference (latency simulation)
  ↓
Metrics Monitor (FPS + memory)
```

---

## Module Details

### `camera/webcam.py`
- Handles webcam initialization, frame capture, and safe release
- Gracefully handles camera disconnects
- Abstracts hardware access from the main pipeline

---

### `pipeline/sampler.py`
Controls processing rate using time-based gating.

Key function:
- `allow()`
  - Returns `True` only if enough time has passed
  - Intentionally drops frames to enforce target FPS

Why this matters:
- Real-time systems **cannot process every frame**
- Frame dropping is preferred over queue buildup on edge devices

---

### `pipeline/preprocess.py`
Prepares frames for inference.

Operations:
```python
frame = frame.astype(np.float32)
frame = np.transpose(frame, (2, 0, 1))  # HWC → CHW
```

Purpose:
- Converts image to float tensor
- Reorders channels to match deep learning model input format
- Mimics preprocessing required by CNN-based models

---

### `inference/dummy_inference.py`
- Simulates model inference using `time.sleep()`
- Introduces artificial latency without a real ML model

This allows:
- Measuring FPS degradation due to inference
- Stress-testing the pipeline before real model integration

---

### `utils/metrics.py`
Enhanced monitoring utilities.

Features:
- FPS calculation
- Memory usage tracking
- `log()` method for periodic reporting
- `reset()` support for metric re-initialization

Explicit timer initialization is required:
```python
monitor.start = time.time()
```

This ensures **accurate FPS computation**, not estimated values.

---

## Main Execution (`main.py`)

Pipeline steps:
1. Capture frame from webcam
2. Check sampler permission (FPS limiting)
3. Preprocess frame
4. Run dummy inference
5. Update and log performance metrics

Example output:
```
FPS: 9.85 | Memory: 312.40 MB
```

The pipeline handles:
- Camera disconnections
- Intentional frame dropping
- Clean shutdown on keyboard interrupt

---

## Key Learnings from Day 3
- Inference latency directly impacts FPS
- Frame sampling is essential for stability
- Preprocessing must match model tensor expectations
- Monitoring must be explicit and continuous

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

Press `Ctrl+C` to stop and release the camera safely.

---

## Outcome
- Fully modular real-time camera pipeline
- Controlled FPS using time-based sampling
- Clear performance impact of inference latency
- Ready foundation for real model integration (Day 4)
