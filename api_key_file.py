import os

class ApiKeyFile:
    def __init__(self):
        self.filename = os.path.expanduser("~/.chatGPT/openai")
        self.api_key = None
        
    def get_api_key(self):
        if self.api_key is None:
            with open(self.filename, 'r') as f:
                self.api_key = f.read().strip()
        return self.api_key

