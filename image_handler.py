import requests

class ImageHandler:
    """
    A class for handling image creation and variations using the OpenAI Images API.
    """
    
    def __init__(self, api_key):
        self.api_key = api_key
        self.endpoint_generation = "https://api.openai.com/v1/images/generations"
        self.endpoint_variation = "https://api.openai.com/v1/images/variations"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}"
        }
        self.image_sizes = {"small": "256x256", "medium": "512x512", "large": "1024x1024"}

    def _send_request(self, endpoint, data, files=None):
        headers = self.headers.copy()
        headers["Content-Type"] = "application/json"
        response = requests.post(endpoint, headers=headers, json=data, files=files)
        response.raise_for_status()
        return response.json()["data"]

    def generate_image(self, prompt, size="medium", n=1, response_format="url"):
        data = {
            "model": "image-alpha-001",
            "prompt": prompt,
            "size": self.image_sizes[size],
            "n": n,
            "response_format": response_format,
        }
        return self._send_request(self.endpoint_generation, data)

    def generate_variation(self, image_path, n=1, size="medium", response_format="url"):
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
            return response.json()["data"]


if __name__ == "__main__":
    # example usage
    handler = ImageHandler(api_key="API_KEY")
    image = handler.generate_image("PROMPT", size="medium")
