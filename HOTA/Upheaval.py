import pyautogui
import cv2
import numpy as np
import time
import keyboard
import json
from pynput import mouse
import threading

enabled = [True]

class ImageWatcher:

    def __init__(self, reference_image_path, region, keys, threshold=0.35, interval=None):
        # ... (rest of the initialization)
        self.interval = interval
        self.region = tuple(region)
        self.keys = keys
        self.threshold = threshold
        self.reference_image = cv2.imread(reference_image_path, cv2.IMREAD_GRAYSCALE)
        self.thread = threading.Thread(target=self.run)
        self.thread.daemon = True  # daemon threads will be killed once the main program exits
        self.thread.start()

    def run(self):
        global enabled
        while True:
            if enabled[0]:
                self.check_image()
            if self.interval:
                time.sleep(self.interval)
            else:
                time.sleep(0.1)

    def check_image(self):
        # Take a screenshot of the specified region and convert it to grayscale
        screenshot = pyautogui.screenshot(region=self.region)
        screenshot.save(f'{self.keys}_screenshot.png')  # Save the screenshot for debugging
        screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2GRAY)

        # Apply template Matching
        print("Screenshot size: ", screenshot.shape)
        print("Reference image size: ", self.reference_image.shape)

        res = cv2.matchTemplate(screenshot, self.reference_image, cv2.TM_CCOEFF_NORMED)
        loc = np.where(res >= self.threshold)

        # If a match is found, press the key
        if len(loc[0]) > 0:
            for key in self.keys:
                if key in ['1', '2', '3']:
                    #sleep for 10 seconds
                    time.sleep(5)
                pyautogui.press(key)
                time.sleep(0.1)  # 100ms delay between key presses
            return True
        return False

# Load the configuration from the JSON file
with open('config.json') as f:
    config = json.load(f)

# Create ImageWatcher instances for each set of parameters
watchers = [ImageWatcher(item['image_path'], item['region'], item['keys'], interval=item.get('interval')) for item in config]

# Start off with the script enabled
enabled = [True]

def toggle_enabled(e):
    enabled[0] = not enabled[0]
    print(f"Script is now {'enabled' if enabled[0] else 'disabled'}")

def press_two(x, y, button, pressed):
    if enabled[0] and button == mouse.Button.left and pressed:
        pyautogui.press('4')

# Start listening for the numlock key to toggle the script
keyboard.on_press_key('numlock', toggle_enabled)
#mouse_listener = mouse.Listener(on_click=press_two)
#mouse_listener.start()

try:
    while True:
        time.sleep(1)  # main thread just waits, individual threads do the work
except KeyboardInterrupt:
    time.sleep(0.1)  # Wait a little between each check to not use 100% CPU