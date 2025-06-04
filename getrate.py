import subprocess
import time
from collections import defaultdict

# Start candump
cmd = ["candump", "-t", "a", "can0"]
proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, text=True)

msg_counts = defaultdict(int)
start_time = time.time()

try:
    while True:
        line = proc.stdout.readline().strip()
        if not line:
            continue

        parts = line.split()
        if len(parts) < 3:
            continue

        can_id = parts[2]
        msg_counts[can_id] += 1

        elapsed = time.time() - start_time
        if elapsed >= 1.0:  # Print rates every second
            print("\nCAN Message Rates (messages per second):")
            for can_id, count in msg_counts.items():
                print(f"ID {can_id}: {count} msg/sec")
            msg_counts.clear()
            start_time = time.time()

except KeyboardInterrupt:
    proc.terminate()
