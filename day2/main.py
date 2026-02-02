from pipeline.loader import load_image_paths
from pipeline.stream import image_stream
from utils.monitor import system_stats, FPSCounter
import time

IMAGE_DIR = "data/images"
paths = load_image_paths(IMAGE_DIR)

# Step 5: Final Batch size of 4
stream = image_stream(paths, batch_size=4)
fps = FPSCounter()
fps.start_timer()

print("Starting Final Batched Pipeline...")
for batch in stream:
    # Simulate processing time for the batch
    time.sleep(0.2) 
    
    # Update FPS by the actual number of images processed in this batch
    fps_val = fps.update(count=len(batch))
    mem = system_stats()
    
    print(f"Batch Size: {len(batch)} | Total FPS: {fps_val:.2f} | Mem(MB): {mem:.2f}")