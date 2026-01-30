# optimisation.py
import torch
from torchvision.models import mobilenet_v2

# Config
ONNX_OUT = "mobilenet_fp16.onnx"

# 1️⃣ Load FP32 model
model = mobilenet_v2()
model.load_state_dict(torch.load("mobilenet_fp32.pth", map_location="cpu"))
model.eval()

# 2️⃣ Convert to FP16
model = model.half()
print("[INFO] Model converted to FP16")

# 3️⃣ Export to ONNX
dummy_input = torch.randn(1, 3, 224, 224).half()

torch.onnx.export(
    model,
    dummy_input,
    ONNX_OUT,
    export_params=True,
    opset_version=13,
    do_constant_folding=True,
    input_names=["input"],
    output_names=["output"],
    dynamic_axes={
        "input": {0: "batch"},
        "output": {0: "batch"}
    }
)

print(f"[INFO] FP16 ONNX model saved as {ONNX_OUT}")
