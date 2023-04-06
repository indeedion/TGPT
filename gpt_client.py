import requests
from typing import Union
from image_handler import ImageHandler


class GPTClient:
    def __init__(self, api_key, model="gpt-3.5-turbo"):
        self.api_key = api_key
        self.endpoint_completions = "https://api.openai.com/v1/chat/completions"
        self.model = model
        self.chat_history = []
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"}
        self.image_handler = ImageHandler(self.api_key)

    def completion(self, prompt, n=1, max_tokens=100, temperature=0.7, top_p=1, frequency_penalty=0, presence_penalty=0, stop=None):
        payload = {
            "model": self.model,
            "messages": [],
            "max_tokens": max_tokens,
            "temperature": temperature,
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
        
        response = requests.post(self.endpoint_completions, headers=self.headers, json=payload)
        response.raise_for_status()

        result = response.json()
        text = [choice['message']['content'] for choice in result['choices']]
        self.add_to_chat_history(prompt, text)
        return text

    def add_to_chat_history(self, prompt, response):
        prompt_message = {'role': 'user', 'content': prompt}
        
        if isinstance(response, list):
            response = response[0]  # Only store the first response in the chat history

        response_message = {'role': 'assistant', 'content': response}
        self.chat_history.append(prompt_message)
        self.chat_history.append(response_message)

    def get_chat_history(self):
        return self.chat_history

    def generate_image(self, prompt, size="medium", n=1, response_format="url"):
        return self.image_handler.generate_image(prompt, n=n, response_format=response_format, size=size)

    def generate_variation(self, image_path: str, n: int = 1, size="medium", response_format: str = "url") -> Union[str, bytes]:
        return self.image_handler.generate_variation(image_path, n=n, size=size, response_format=response_format)


if __name__ == "__main__":
    client = GPTClient(api_key="API_KEY")
    response = client.completion("Hello, how are you?", max_tokens=100)
    print(response)
