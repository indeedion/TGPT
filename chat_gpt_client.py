import openai
import requests
import json
import uuid
import time
import io
import base64
import tempfile
import os
import datetime
from typing import Union
from api_key_file import ApiKeyFile
from image_handler import ImageHandler
from openai import OpenAIError
#from openai import OpenAIAPIException

class ChatGPTClient:
    """
    This class provides a client to interact with the GPT-3 API.
    
    Attributes:
        api_key (str): The API key for the GPT-3 API.
        model (str): The GPT-3 model to use for generating text.
        endpoint (str): The API endpoint for completions.
        chat_history (list): A list of chat history messages.
        headers (dict): Headers for API requests.
    """

    def __init__(self, api_key, model="gpt-3.5-turbo", endpoint="https://api.openai.com/v1/chat/completions"):
        """
        Initializes the ChatGPTClient instance with the provided API key, model, and endpoint.
        
        :param api_key: The GPT-3 API key.
        :param model: The GPT-3 model to use for generating text (default: "gpt-3.5-turbo").
        :param endpoint: The API endpoint for completions (default: "https://api.openai.com/v1/chat/completions").
        """
        self.api_key = api_key
        self.endpoint = endpoint
        self.model = model
        self.chat_history = []
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"}
        self.image_handler = ImageHandler(api_key)
        
    def prompt(self, prompt, chat_log=None, stop=None, max_tokens=100, temperature=0.5, top_p=1):
        """
        Sends a prompt to the GPT-3 API to generate a completion.
        
        :param prompt: The prompt to send to the API.
        :param chat_log: Optional; the previous conversation history in the chat format.
        :param stop: Optional; up to 4 sequences where the API will stop generating further tokens.
        :param max_tokens: The maximum number of tokens to generate in the completion (default: 100).
        :param temperature: The sampling temperature to use, between 0 and 1 (default: 0.5).
        :param top_p: An alternative to sampling with temperature (default: 1).
        :return: The response from the API, containing the generated text.
        """
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.api_key}'
        }

        payload = {
            'model': 'gpt-3.5-turbo',
            'prompt': prompt,
            'temperature': temperature,
            'max_tokens': max_tokens,
            'top_p': top_p
        }

        if stop is not None:
            payload['stop'] = stop

        if chat_log is not None:
            payload['messages'] = chat_log

        url = 'https://api.openai.com/v1/chat/completions'
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()

        data = response.json()['choices'][0]['text']
        return data.strip()

        
    def completions(self, prompt, max_tokens=100, temperature=0.5, top_p=1, presence_penalty=0, frequency_penalty=0, stop=None, n=1):
        """
        Generates completions based on the given prompt.
        
        :param prompt: The user's prompt.
        :param max_tokens: The maximum number of tokens to generate in the completion (default: 100).
        :param temperature: The sampling temperature to use, between 0 and 1 (default: 0.5).
        :param top_p: An alternative to sampling with temperature (default: 1).
        :param presence_penalty: Controls how much the model should consider token presence (default: 0).
        :param frequency_penalty: Controls how much the model should consider token frequency (default: 0).
        :param stop: Optional; up to 4 sequences where the API will stop generating further tokens.
        :param n: The number of completions to generate for each prompt (default: 1).
        :return: The generated text from the completion.
        """
        headers = {"Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}"}
        data = {
            "model": self.model,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "top_p": top_p,
            "n": n,
            "presence_penalty": presence_penalty,
            "frequency_penalty": frequency_penalty,
            "stop": stop
        }

        messages = [{"role": "user", "content": prompt}]
        data["messages"] = messages

        url = "https://api.openai.com/v1/chat/completions"
        response = requests.post(url, headers=headers, json=data)
        if response.status_code != 200:
            print(response.content.decode())
            raise ValueError("Failed to generate completions")
        response = response.json()
        choices = response["choices"]
        return choices[0]["message"]["content"].strip()

    def generate_text(self, prompt, max_tokens=200, temperature=0.5, top_p=1, frequency_penalty=0, presence_penalty=0):
        """
        Generates text based on the given prompt.
        
        :param prompt: The user's prompt.
        :param max_tokens: The maximum number of tokens to generate in the completion (default: 200).
        :param temperature: The sampling temperature to use, between 0 and 1 (default: 0.5).
        :param top_p: An alternative to sampling with temperature (default: 1).
        :param frequency_penalty: Controls how much the model should consider token frequency (default: 0).
        :param presence_penalty: Controls how much the model should consider token presence (default: 0).
        :return: The generated text from the completion.
        """
        payload = {
            "model": self.model,
            "messages": [],
            "max_tokens": max_tokens,
            "temperature": temperature,
            "top_p": top_p,
            "frequency_penalty": frequency_penalty,
            "presence_penalty": presence_penalty
        }

        if self.chat_history:
            history = self.chat_history
            history.append({"role": "user", "content": prompt})
            payload["messages"] = history
        else:
            payload["messages"] = [{"role": "user", "content": prompt}]
        
        
        response = requests.post(self.endpoint, headers=self.headers, json=payload)

        #print(payload)
        #print(response.content.decode())

        response.raise_for_status()

        result = response.json()
        choices = result["choices"]
        text = choices[0]["message"]["content"].strip()
        self.add_to_chat_history(prompt, text)
        return text

    def add_to_chat_history(self, prompt, response):
        """
        Adds a prompt and response message to the chat history.
        
        :param prompt: The user's prompt.
        :param response: The generated response from the model.
        """
        prompt_message = {'role': 'user', 'content': prompt}
        response_message = {'role': 'assistant', 'content': response}
        self.chat_history.append(prompt_message)
        self.chat_history.append(response_message)

    def get_chat_history(self):
        """
        Retrieves the current chat history.
        
        :return: A list of dictionaries containing chat history messages.
        """
        return self.chat_history

    def generate_image(self, prompt, size="256x256", n=1, response_format="url"):
        """
        Generates an image based on the specified text prompt.

        :param prompt: The text prompt to generate the image from.
        :param size: The size of the generated image. Can be one of "256x256", "512x512", or "1024x1024".
        :param n: The number of images to generate.
        :param response_format: The format of the response. Can be one of "url" or "base64".
        :return: The generated image(s), either as a URL or base64-encoded data.
        """
        return self.image_handler.generate_image(prompt, size, n, response_format)

    def generate_variation(self, image_path: str, n: int = 1, size: str = "512x512", response_format: str = "url") -> Union[str, bytes]:
        """
        Generates a variation of a given image.
        
        :param image_path: The file path to the input image.
        :param n: The number of images to generate (default 1).
        :param size: The size of the generated image in pixels (default "512x512").
        :param response_format: The format in which to return the generated image, either "url" or "base64" (default "url").
        :return: The URL or Base64-encoded string of the generated image, depending on the value of response_format.
        """

        return self.image_handler.generate_variation(image_path, n=n, size=size, response_format=response_format)

    def save_image(self, image_url, file_path):
        """
        Saves the image from the provided URL to a local file.

        :param image_url: The URL of the image to save.
        :param file_path: The local file path to save the image to.
        """
        response = requests.get(image_url)
        with open(file_path, "wb") as f:
            f.write(response.content)

    def get_image_data(self, image_url: str) -> bytes:
        # Download the image from the URL and save it to a file
        now = datetime.datetime.now()
        date_str = now.strftime("%Y-%m-%d-%H:%M:%S")
        image_name = f"gpt-gen-{date_str}.png"
        pictures_dir = os.path.expanduser("~/Pictures/TerminalGPT")
        if not os.path.exists(pictures_dir):
            os.makedirs(pictures_dir)
        response = requests.get(image_url)
        image_file = os.path.join(f"{pictures_dir}/{image_name}")
        with open(image_file, "wb") as f:
            f.write(response.content)
            print(f"Image saved to file {pictures_dir}/{image_name}")
        # Open the file and return its contents
        with open(image_file, "rb") as f:
            return f.read()
 
if __name__ == "__main__":
    api_key_file = ApiKeyFile()
    api_key = api_key_file.get_api_key()
    client = ChatGPTClient(api_key)
    print(client.get_engine())
    # Use client methods here

#/home/indeedion/Pictures/TerminalGPT