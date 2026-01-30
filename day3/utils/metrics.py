# metrics.py
# Responsibility:
# - Track frames per second (FPS)
# - Track memory used (MB)

import time
import psutil


class Monitor:
    def __init__(self):
        """
        Initialize frame counter and time tracker.

        Think:
        - Why track both frames and time?
        - Why not reset every second?
        """
        # TODO:
        # 1. Start time reference
        self.start = time.time()

        # 2. Frame counter
        self.frames = 0

    def update(self):
        """
        Call this once per frame.

        Returns:
        - Current average FPS
        - Current memory usage in MB

        Think:
        - Why report both together?
        - What might cause memory to rise over time?
        """

        # TODO:
        # 1. Increment frame count
        self.frames += 1

        # 2. Calculate elapsed time
        elapsed = time.time() - self.start
        fps = self.frames / elapsed if elapsed > 0 else 0.0

        # 3. Get used memory via psutil
        mem_mb = psutil.virtual_memory().used / (1024 * 1024)

        # 4. Return (fps, mem_mb)
        return fps, mem_mb
     
    def reset(self):
        """
        Reset FPS tracking.
        """
        self.start = time.time()
        self.frames = 0   # ✅ fixed name

    def log(self, fps, mem_mb, every_n=10, path="metrics.log"):
        """
        Log metrics every N frames.
        """
        if self.frames % every_n != 0:
            return

        with open(path, "a") as f:
            f.write(
                f"{time.time():.2f}, "
                f"{self.frames}, "
                f"{fps:.2f}, "
                f"{mem_mb:.2f}\n"
            )
