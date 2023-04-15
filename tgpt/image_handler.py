import requests
import os
import urllib
from datetime import datetime


class ImageHandler:
    """
    A handler for generating and saving images from the OpenAI API.
    
    Attributes:
        api_key (str): The OpenAI API key.
    """
    def __init__(self, api_key):
        """
        Initialize the ImageHandler with the given API key.
        """
        self.api_key = api_key
        self.endpoint_generation = "https://api.openai.com/v1/images/generations"
        self.endpoint_variation = "https://api.openai.com/v1/images/variations"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}"
        }
        self.image_sizes = {"small": "256x256", "medium": "512x512", "large": "1024x1024"}

    def _send_request(self, endpoint, data, files=None):
        """
        Send a request to the OpenAI API endpoint with the provided data.
        
        Returns:
            list: A list containing the JSON response data.
        """
        try:
            headers = self.headers.copy()
            headers["Content-Type"] = "application/json"
            response = requests.post(endpoint, headers=headers, json=data, files=files)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Error making request to OpenAI API: {e}")
            return []

        try:
            return response.json()["data"]
        except Exception as e:
            print(f"Error processing OpenAI API response: {e}")
            return []

    def generate_image(self, prompt, size="medium", n=1, response_format="url", save_path=None):
        """
        Generate an image based on the given prompt and save it to the specified location.
        
        Returns:
            list: A list of file paths where the generated images are saved.
        """
        data = {
            "model": "image-alpha-001",
            "prompt": prompt,
            "size": self.image_sizes[size],
            "n": n,
            "response_format": response_format,
        }

        try:
            response = self._send_request(self.endpoint_generation, data)
        except Exception as e:
            print(f"Error generating image: {e}")
            return []
        
        timestamp = datetime.now().strftime("%Y:%m-%d-%H:%M:%S")
        save_paths = []

        if save_path is None:
            save_path = os.getcwd()

        if response:
            for i, image_url in enumerate(response):
                save_paths.append(self.save_image(image_url, os.path.join(save_path, f"gpt-generate-{i}-{timestamp}.png")))

        return save_paths

    def generate_variation(self, image_name, n=1, size="medium", response_format="url", save_path=None):
        """
        Generate a variation of the given image and save it to the specified location.
        
        Returns:
            list: A list of file paths where the generated image variations are saved.
        """
        if os.path.isabs(image_name):
            image_path = image_name
        else:
            current_folder = os.getcwd()
            image_path = os.path.join(current_folder, image_name)
        try:
            with open(image_path, 'rb') as image_file:
                data = {
                    "n": n,
                    "size": self.image_sizes[size],
                    "response_format": response_format,
                }
                files = {"image": image_file}
                headers = self.headers.copy()
                response = requests.post(self.endpoint_variation, headers=headers, data=data, files=files)
                response.raise_for_status()

                timestamp = datetime.now().strftime("%Y:%m-%d-%H:%M:%S")
                save_paths = []

                if save_path is None:
                    save_path = os.getcwd()

                if response.json()["data"]:
                    for i, image_url in enumerate(response.json()["data"]):
                        save_paths.append(self.save_image(image_url, os.path.join(save_path, f"gpt-variation-{i}-{timestamp}.png")))

            return save_paths
        except Exception as e:
            print(f"Error generating image variation: {e}")
            return []

    def save_image(self, url, file_path, timeout=30):
        """
        Save the image from the provided URL to the specified file path.
        
        Returns:
            str: The file path where the image is saved.
        """
        try:
            with urllib.request.urlopen(url['url'], timeout=timeout) as response, open(file_path,'wb') as out_file:
                out_file.write(response.read())
                print(f"\nSaved image to {file_path}")
                return file_path
        except Exception as e:
            print(f"An error occurred while saving the image: {e}")

if __name__ == "__main__":
    try:
        handler = ImageHandler(api_key="API_KEY")
        image = handler.generate_image("PROMPT", size="medium", save_path="path/to/save/images")
    except Exception as e:
        print(f"Error initializing ImageHandler or generating image: {e}")
