# main_onnx.py
# Orchestrates live MobileNet FP16 ONNX pipeline with FPS monitoring

from camera.webcam import Webcam
from pipeline.sampler import FrameSampler
# from pipeline.preprocess import preprocess
from inference.mobilenet import MobileNetONNXInference
from app_utils.metrics import Monitor
from app_utils.labels import load_labels

# -------------------------
# Init
# -------------------------
quantized_model_path = "mobilenet_fp16.onnx"

cam = Webcam(0, 640, 480)
sampler = FrameSampler(target_fps=5)
monitor = Monitor()
model = MobileNetONNXInference(quantized_model_path)
labels = load_labels()

print("[INFO] Using ONNX FP16 model")

# -------------------------
# Main loop
# -------------------------
try:
    while True:
        # 1️⃣ Read frame
        frame = cam.read()
        if frame is None:
            continue

        # 2️⃣ Throttle FPS
        if not sampler.allow():
            continue

        # 3️⃣ Preprocess
        img = frame

        # 4️⃣ ONNX inference
        probs = model.predict(img)

        # 5️⃣ Decode prediction
        top = probs.argmax().item()
        label = labels[top]

        # 6️⃣ FPS + memory
        fps, mem = monitor.update()
        print(f"Prediction: {label} | FPS: {fps:.2f} | Mem: {mem:.2f} MB")

except KeyboardInterrupt:
    cam.release()
    print("[INFO] Camera stopped. Exiting.")
