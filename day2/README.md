# Edge Data Pipeline

A memory-efficient Python pipeline designed for Edge AI devices (like NVIDIA Jetson).

## Core Principles Implemented:
1. **Lazy Loading:** Discovers file paths without loading images into RAM.
2. **Generators:** Uses Python `yield` to process one image at a time, keeping memory usage constant.
3. **Optimized Preprocessing:** Resizes images to `224x224` early to reduce compute load.
4. **Performance Monitoring:** Tracks real-time FPS and Memory usage.

## How to Run
1. Install dependencies: `pip install -r requirements.txt`
2. Run the pipeline: `python3 main.py`