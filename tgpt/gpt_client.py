import requests
from typing import Union
from .image_handler import ImageHandler


class GPTClient:
    def __init__(self, api_key, model="gpt-3.5-turbo", max_tokens=100, temperature=0.7):
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
        self.max_tokens = max_tokens

    def get_max_tokens(self):
        return self.max_tokens

    def set_temperature(self, temperature):
        self.temperature = temperature

    def get_temperature(self):
        return self.temperature

    def get_model(self):
        return self.model
    
    def get_chat_history(self):
        return self.chat_history

    def add_to_chat_history(self, prompt, response):
        prompt_message = {'role': 'user', 'content': prompt}
        
        if isinstance(response, list):
            response = response[0]  # Only store the first response in the chat history

        response_message = {'role': 'assistant', 'content': response}
        self.chat_history.append(prompt_message)
        self.chat_history.append(response_message)

    def generate_image(self, prompt, size="medium", n=1, response_format="url", save_path = None):
        return self.image_handler.generate_image(prompt, n=n, response_format=response_format, size=size, save_path=save_path)

    def generate_variation(self, image_name: str, n: int = 1, size="medium", response_format: str = "url", save_path = None) -> Union[str, bytes]:
        return self.image_handler.generate_variation(image_name, n=n, size=size, response_format=response_format, save_path=save_path)
    
    #def save_image(self, url, file_path, timeout = 30):
        #self.image_handler.save_image(url, file_path, timeout)


if __name__ == "__main__":
    try:
        client = GPTClient(api_key="API_KEY")
        response = client.completion("Hello, how are you?", max_tokens=100)
        print(response)
    except Exception as e:
        print(f"Error initializing GPTClient or making completion request: {e}")