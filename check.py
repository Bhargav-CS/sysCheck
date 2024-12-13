import mss
import time

def capture_screenshot(filename="screenshot.png"):
    with mss.mss() as sct:
        sct.shot(output=filename)

# Test
while True:
    capture_screenshot()
    print("Screenshot captured")
    time.sleep(20)  # Capture every 2 minutes
