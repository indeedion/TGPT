import os
import time
import subprocess
from config_handler import ConfigHandler

# Get config for API key and set sleeptime, so the API doesn't get spammed
config = ConfigHandler()
sleep_time = 6

# Replace these values with your actual API key and valid paths
API_KEY = config.get_api_key()
IMAGE_PATH = os.path.abspath("/tmp/gpt-generate-0-2023:04-15-02:19:35.png")
SAVE_PATH = os.path.abspath("/tmp/")

def test_command(command):
    print(f"Running command: {' '.join(command)}")
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}, Output: {e.output}")

def run_and_sleep(command, sleep_time):
    test_command(command)
    time.sleep(sleep_time)

def main():
    # Test the text query functionality
    run_and_sleep(["tgpt", "tx", "What is the capital of France?"], sleep_time)
    run_and_sleep(["tgpt", "tx", "What is the capital of France?", "-n", "2"], sleep_time)
    run_and_sleep(["tgpt", "tx", "What is the capital of France?", "-t", "0.5"], sleep_time)
    run_and_sleep(["tgpt", "tx", "\"What is the capital of France?\"", "-m", "200"], sleep_time)

    # Test the generate image functionality
    run_and_sleep(["tgpt", "gi", "\"A beautiful sunset over the ocean\""], sleep_time)
    run_and_sleep(["tgpt", "gi", "\"A beautiful sunset over the ocean\"", SAVE_PATH, "-s", "small", "-n", "2"], sleep_time)

    # Test the generate variation functionality
    run_and_sleep(["tgpt", "gv", IMAGE_PATH], sleep_time)
    run_and_sleep(["tgpt", "gv", IMAGE_PATH, SAVE_PATH, "-s", "large", "-n", "2" ], sleep_time)


if __name__ == "__main__":
    main()
