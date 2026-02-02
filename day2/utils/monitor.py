import psutil
import time

def system_stats():
    """Rule 5: Measure memory in MB."""
    return psutil.virtual_memory().used / (1024 * 1024)

class FPSCounter:
    def __init__(self):
        self.start = None
        self.frames = 0
    def start_timer(self):
        self.start = time.time()
    def update(self, count=1):
        # Increment by the number of images in the batch
        self.frames += count
        elapsed = time.time() - self.start
        return self.frames / elapsed if elapsed > 0 else 0.0