import openai
import requests
from io import BytesIO
from PIL import Image

class ImageHandler:
    """
    A class for handling image creation, editing, and variations using the OpenAI Images API.
    """
    
    def __init__(self, api_key):
        """
        Initializes the ImageHandler instance with the provided OpenAI API key.
        
        :param api_key: The OpenAI API key.
        """
        self.model = "gpt-3.5-turbo"
        self.api_key = api_key
        self.endpoint = "https://api.openai.com/v1/images/generations"
        self.endpoint_edit = "https://api.openai.com/v1/images/edits"
        self.endpoint_variation = "https://api.openai.com/v1/images/variations"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}"
        }
        
    def generate_image(self, prompt, size="512x512", n=1, response_format="url"):
        """
        Generates an image based on the provided prompt using the OpenAI Images API.
        
        :param prompt: The text prompt for generating the image.
        :param size: The size of the generated image. Can be "256x256", "512x512", or "1024x1024". Default is "512x512".
        :param n: The number of images to generate. Default is 1.
        :param response_format: The format of the response. Can be "url" or "base64". Default is "url".
        
        :return: A list of generated image URLs or base64-encoded image data.
        """
        headers = {"Content-Type": "application/json", "Authorization": f"Bearer {self.api_key}"}
        data = {
            "model": "image-alpha-001",
            "prompt": prompt,
            "size": size,
            "n": n,
            "response_format": response_format,
        }
        
        response = requests.post(self.endpoint, headers=headers, json=data)
        response.raise_for_status()
        return response.json()["data"]

    def generate_variation(self, image_path, n=1, size="512x512", response_format="url"):
        """
        Generates a variation of an existing image.

        :param image_file: The file object or file path of the image to generate a variation of.
        :param n: The number of images to generate (default 1).
        :param size: The size of the generated images (default "512x512").
        :param response_format: The format of the response (default "url").
        :return: A list of URLs or base64-encoded image data, depending on the response format.
        """
        if isinstance(image_path, str):
            # If image_file is a string, assume it's a file path and open the file
            image_file = open(image_path, 'rb')

        # Build the request data
        data = {
            "n": n,
            "size": size,
            "response_format": response_format,        
        }
        files = {"image": image_file}

        # Make the API request
        response = requests.post(self.endpoint_variation, data=data, files=files, headers=self.headers)
        #print(response.content.decode())
        response.raise_for_status()

        # Parse the response and return the image URLs or base64-encoded data
        return response.json()["data"]
        


