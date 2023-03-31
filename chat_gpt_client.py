import openai
import requests
import json
import uuid
import time
from api_key_file import ApiKeyFile
from openai import OpenAIError
#from openai import OpenAIAPIException

class ChatGPTClient:
    def __init__(self, api_key, model="gpt-3.5-turbo", endpoint="https://api.openai.com/v1/chat/completions"):
        self.api_key = api_key
        self.endpoint = endpoint
        self.model = model
        self.chat_history = []
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"}
        
        def prompt(self, prompt, chat_log=None, stop=None, max_tokens=100, temperature=0.5, top_p=1):
            """
            Send a prompt to the GPT-3 API to generate a completion.

            Args:
                prompt (str): The prompt to send to the API.
                chat_log (Optional[str]): The previous conversation history in the chat format. 
                                        Use only for chat mode.
                stop (Optional[str or List[str]]): Up to 4 sequences where the API will stop generating further tokens.
                max_tokens (int): The maximum number of tokens to generate in the completion.
                temperature (float): What sampling temperature to use, between 0 and 1.
                top_p (float): An alternative to sampling with temperature, where the model 
                            considers the results of the tokens with top_p probability mass.

            Returns:
                The response from the API, containing the generated text.
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
        headers = {"Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}"}
        data = {
            "model": self.model,
            "prompt": prompt,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "top_p": top_p,
            "n": n,
            "presence_penalty": presence_penalty,
            "frequency_penalty": frequency_penalty,
            "stop": stop
        }
        url = "https://api.openai.com/v1/chat/completions"
        response = requests.post(url, headers=headers, json=data)
        if response.status_code != 200:
            raise ValueError("Failed to generate completions")
        response = response.json()
        choices = response["choices"]
        return [choice["text"].strip() for choice in choices]

    def generate_text(self, prompt, max_tokens=200, temperature=0.5, top_p=1, frequency_penalty=0, presence_penalty=0):
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
            payload["messages"] = self.chat_history
        else:
            payload["messages"] = [{"role": "user", "content": prompt}]
        
        response = requests.post(self.endpoint, headers=self.headers, json=payload)
        response.raise_for_status()
        result = response.json()
        choices = result["choices"]
        text = choices[0]["message"]["content"].strip()
        self.add_to_chat_history(prompt, text)
        return text

    def set_api_key(self, api_key):
        self.api_key = api_key

    def set_model(self, model):
        self.model = model

    def list_models(self):
        url = "https://api.openai.com/v1/models"
        headers = {"Authorization": f"Bearer {self.api_key}"}
        response = requests.get(url, headers=headers)
        return [model["id"] for model in response.json()["data"]]

    def add_to_chat_history(self, prompt, response):
        """Adds a prompt and response message to the chat history."""
        prompt_message = {'role': 'user', 'content': prompt}
        response_message = {'role': 'assistant', 'content': response}
        self.chat_history.append(prompt_message)
        self.chat_history.append(response_message)

    def get_chat_history(self):
        return self.chat_history
 
if __name__ == "__main__":
    api_key_file = ApiKeyFile()
    api_key = api_key_file.get_api_key()
    client = ChatGPTClient(api_key)
    print(client.get_engine())
    # Use client methods here

