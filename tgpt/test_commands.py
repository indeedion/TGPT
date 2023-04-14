import os
import sys
import time
import subprocess
from config_handler import ConfigHandler

# Get config for API key
config = ConfigHandler()
current_folder = os.getcwd()

# Replace these values with your actual API key and valid paths
API_KEY = config.get_api_key()
IMAGE_PATH = os.path.abspath(f"{current_folder}/../image_tests/gpt-generate-0-2023:04-14-22:15:23.png")
SAVE_PATH = os.path.abspath(f"{current_folder}/../image_tests/")

def test_command(command):
    print(f"Running command: {' '.join(command)}")
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}, Output: {e.output}")

def main():
    # Test the text query functionality
    test_command(["tgpt", "tx", "What is the capital of France?"])
    time.sleep(5)  # Add a delay of 5 seconds
    test_command(["tgpt", "tx", "What is the capital of France?", "-n", "2"])
    time.sleep(5)
    test_command(["tgpt", "tx", "What is the capital of France?", "-t", "0.5"])
    time.sleep(5)
    test_command(["tgpt", "tx", "What is the capital of France?", "-m", "200"])
    time.sleep(5)

    # Test the generate image functionality
    test_command(["tgpt", "gi", "\"A beautiful sunset over the ocean\""])
    time.sleep(5)
    test_command(["tgpt", "gi", "\"A beautiful sunset over the ocean\"", SAVE_PATH, "-s", "small", "-n", "2"])
    time.sleep(5)

    # Test the generate variation functionality
    test_command(["tgpt", "gv", IMAGE_PATH])
    time.sleep(5)
    test_command(["tgpt", "gv", IMAGE_PATH, SAVE_PATH, "-s", "large", "-n", "2" ])


if __name__ == "__main__":
    main()
