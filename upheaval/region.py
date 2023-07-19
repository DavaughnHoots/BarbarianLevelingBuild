import pyautogui
import keyboard
import json

def set_region(e, config, i):
    # This function will be called when the F1 key is pressed
    # It sets the region to a 120x120 square around the current mouse position
    x, y = pyautogui.position()
    region = [x - 60, y - 60, 120, 120]  # Adjusted for 120x120 region

    print(f'Setting region for {config[i]["key"]} to {region}')  # Debug statement

    # Update the region in the configuration
    config[i]['region'] = region

    # Save the configuration to the JSON file
    with open('config.json', 'w') as f:
        json.dump(config, f, indent=4)

# Load the configuration from the JSON file
with open('config.json') as f:
    config = json.load(f)

# Start listening for the F1 key for each watcher
for i, item in enumerate(config):
    print(f'Press F{str(i + 1)} to set the region for {item["key"]}')
    keyboard.on_press_key(
        f'f{str(i + 1)}', lambda e: set_region(e, config, i)
    )

# Block the script from exiting
keyboard.wait()
