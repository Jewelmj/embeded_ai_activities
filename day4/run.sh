#!/bin/bash
# run.sh - Setup and run MobileNet Edge Inference Pipeline on Jetson Nano

echo "[INFO] Activating virtual environment (optional)..."
# Uncomment if using venv
# source venv/bin/activate

echo "[INFO] Installing system dependencies..."
sudo apt-get update
sudo apt-get install -y python3-pip python3-opencv libopencv-dev

echo "[INFO] Installing Python packages..."
pip3 install --upgrade pip
pip3 install torch torchvision psutil

echo "[INFO] Running pipeline..."
python3 main.py