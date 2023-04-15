import requests
from typing import Union
from .image_handler import ImageHandler


class GPTClient:
    """
    A GPT client for interacting with the OpenAI API and performing completions.
    
    Attributes:
        api_key (str): The OpenAI API key.
        model (str): The name of the GPT model to use.
        max_tokens (int): The maximum number of tokens for completions.
        temperature (float): The temperature for completions.
    """
    def __init__(self, api_key, model="gpt-3.5-turbo", max_tokens=100, temperature=0.7):
        """
        Initialize the GPTClient with the given API key and model.
        """
        self.api_key = api_key
        self.endpoint_completions = "https://api.openai.com/v1/chat/completions"
        self.model = model
        self.chat_history = []
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"}
        self.image_handler = ImageHandler(self.api_key)
        self.max_tokens = max_tokens
        self.temperature = temperature


    def completion(self, prompt, n=1, top_p=1, frequency_penalty=0, presence_penalty=0, stop=None):
        """
        Generate a completion for the given prompt using the GPT model.
        
        Returns:
            list: A list containing the completion text.
        """
        payload = {
            "model": self.model,
            "messages": [],
            "max_tokens": self.max_tokens,
            "temperature": self.temperature,
            "top_p": top_p,
            "frequency_penalty": frequency_penalty,
            "presence_penalty": presence_penalty,
            "n": n,
            "stop": stop
        }

        if self.chat_history:
            history = self.chat_history
            history.append({"role": "user", "content": prompt})
            payload["messages"] = history
        else:
            payload["messages"] = [{"role": "user", "content": prompt}]
        
        try:
            response = requests.post(self.endpoint_completions, headers=self.headers, json=payload)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Error making request to GPT API: {e}")
            return []

        try:
            result = response.json()
            text = [choice['message']['content'] for choice in result['choices']]
            self.add_to_chat_history(prompt, text)
            return text
        except Exception as e:
            print(f"Error processing GPT API response: {e}")
            return []
        
    def set_max_tokens(self, max_tokens):
        """
        Set the maximum number of tokens for completions.
        """
        self.max_tokens = max_tokens

    def get_max_tokens(self):
        """
        Retrieve the maximum number of tokens for completions.
        
        Returns:
            int: The maximum number of tokens.
        """
        return self.max_tokens

    def set_temperature(self, temperature):
        """
        Set the temperature for completions.
        """
        self.temperature = temperature

    def get_temperature(self):
        """
        Retrieve the temperature for completions.
        
        Returns:
            float: The temperature.
        """
        return self.temperature

    def get_model(self):
        """
        Retrieve the GPT model name.
        
        Returns:
            str: The GPT model name.
        """
        return self.model
    
    def get_chat_history(self):
        """
        Retrieve the chat history.
        
        Returns:
            list: The chat history.
        """
        return self.chat_history

    def add_to_chat_history(self, prompt, response):
        """
        Add the prompt and response to the chat history.
        """
        prompt_message = {'role': 'user', 'content': prompt}
        
        if isinstance(response, list):
            response = response[0] 

        response_message = {'role': 'assistant', 'content': response}
        self.chat_history.append(prompt_message)
        self.chat_history.append(response_message)

    def generate_image(self, prompt, size="medium", n=1, response_format="url", save_path = None):
        """
        Generate an image based on the prompt.
        
        Returns:
            Union[str, bytes]: The image URL or image bytes, depending on the response_format.
        """
        return self.image_handler.generate_image(prompt, n=n, response_format=response_format, size=size, save_path=save_path)

    def generate_variation(self, image_name: str, n: int = 1, size="medium", response_format: str = "url", save_path = None) -> Union[str, bytes]:
        """
        Generate a variation of the given image.
        
        Returns:
            Union[str, bytes]: The image URL or image bytes, depending on the response_format.
        """
        return self.image_handler.generate_variation(image_name, n=n, size=size, response_format=response_format, save_path=save_path)


if __name__ == "__main__":
    try:
        client = GPTClient(api_key="API_KEY")
        response = client.completion("Hello, how are you?", max_tokens=100)
        print(response)
    except Exception as e:
        print(f"Error initializing GPTClient or making completion request: {e}")