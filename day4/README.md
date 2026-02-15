# Day 4 — Real-Time Models, ONNX Export & Jetson-Oriented Optimization

## Overview
Day 4 represents the **final integration and deployment-focused stage** of the AEC pipeline.  
This activity upgrades the dummy-inference system into a **real-time vision pipeline** using:

- **MobileNetV2** for image classification
- **YOLOv5n** for object detection
- **FP16 optimization + ONNX export** for Jetson-class devices
- Live camera inference with **FPS & memory monitoring**

The primary goal is to demonstrate **end-to-end readiness for edge deployment**, not just model accuracy.

---

## Folder Structure
```
day4/
├── app_utils/
│   ├── labels.py        # ImageNet label loader
│   └── metrics.py       # FPS & memory monitor
├── camera/
│   └── webcam.py        # Live camera interface
├── inference/
│   ├── mobilenet.py     # Torch + ONNX MobileNet inference
│   ├── yolo.py          # YOLOv5 object detection
│   └── test_image_inference.py
├── pipeline/
│   ├── preprocess.py   # Frame preprocessing
│   └── sampler.py      # FPS throttling
├── main.py              # Live MobileNet (FP32) pipeline
├── main_yolo.py         # Live YOLO pipeline
├── optimisation.py      # FP32 → FP16 → ONNX export
├── run_quantised_model.py  # Live ONNX FP16 inference
├── run.sh
├── mobilenet_fp32.pth
└── mobilenet_fp16.onnx
```

> **Note:** `utils` was renamed to `app_utils` to avoid naming conflicts with YOLO dependencies.

---

## Supported Pipelines

### 1️⃣ MobileNet FP32 (Torch)
- File: `main.py`
- Backend: PyTorch
- Device: CPU / CUDA (auto-detected)

Pipeline:
```
Webcam → Sampler → Preprocess → MobileNet → FPS + Memory
```

This serves as the **baseline accuracy and performance reference**.

---

### 2️⃣ MobileNet FP16 (ONNX Runtime)
- File: `run_quantised_model.py`
- Backend: ONNX Runtime
- Precision: FP16
- Providers: CUDA / CPU

Pipeline:
```
Webcam → Sampler → ONNX FP16 MobileNet → FPS + Memory
```

This pipeline reflects **Jetson Nano–style deployment**, prioritizing latency and memory efficiency.

---

### 3️⃣ YOLOv5 Object Detection
- File: `main_yolo.py`
- Backend: PyTorch + `torch.hub`
- Model: `yolov5n.pt`

YOLO is included to demonstrate **multi-task capability** and handling of heavier detection models.

---

## Key Modules Explained

### `app_utils/labels.py`
- Loads ImageNet class labels (0–999)
- Used for decoding MobileNet predictions

---

### `app_utils/metrics.py`
Tracks real-time performance:
```python
fps = count / elapsed
mem = psutil.virtual_memory().used / (1024 ** 2)  # MB
```

Metrics are printed live to validate **real-time feasibility**.

---

### `inference/mobilenet.py`
Supports **two inference backends**:

#### Torch FP32
- Uses `torchvision.models.mobilenet_v2`
- Standard ImageNet normalization
- GPU acceleration when available

#### ONNX FP16
- Uses `onnxruntime`
- FP16 inputs for reduced memory + latency
- CUDAExecutionProvider preferred

This dual-backend design enables **fair performance comparison**.

---

### `optimisation.py` — FP32 → FP16 → ONNX
Steps:
1. Load trained FP32 MobileNet
2. Convert weights to FP16
3. Export to ONNX with dynamic batch support

Why FP16:
- Lower memory footprint
- Faster inference on Jetson GPUs
- Minimal accuracy loss for classification

---

### `run_quantised_model.py`
Runs **live camera inference** using the FP16 ONNX model.

Features:
- FPS throttling
- ONNX Runtime execution
- Real-time label prediction
- Memory monitoring

This is the **closest representation of Jetson Nano deployment**.

---

### `inference/yolo.py`
- Loads YOLOv5 via `torch.hub`
- Handles path resolution robustly
- Demonstrates detection vs classification trade-offs

YOLO runs at lower FPS but offers spatial understanding.

---

## Why This Design is Jetson-Ready
- Explicit FPS throttling
- FP16 inference path
- ONNX Runtime compatibility
- Memory-aware monitoring
- Modular swap between models

Even without physical Jetson hardware, the pipeline matches **industry deployment patterns**.

---

## How to Run

### MobileNet (FP32 Torch)
```bash
python3 main.py
```

### MobileNet (FP16 ONNX)
```bash
python3 run_quantised_model.py
```

### YOLOv5 Detection
```bash
python3 main_yolo.py
```

---

## Outcome
- Real-time classification and detection pipelines
- FP16-optimized ONNX model
- Deployment-aware design for Jetson Nano
- Clear performance trade-off analysis

---

## Final Note
Day 4 demonstrates **system-level thinking**, not just ML usage:
- Model selection
- Optimization
- Deployment constraints
- Performance validation

This completes the AEC pipeline end-to-end.
