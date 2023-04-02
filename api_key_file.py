import os

class ApiKeyFile:
    """
    This class handles the API key stored in a file.

    Attributes:
        filename (str): The file path for the API key file.
        api_key (str): The API key value.
    """
    def __init__(self):
        """
        Initializes the ApiKeyFile instance, setting the API key file path
        and initializing the api_key attribute to None.
        """
        self.filename = os.path.expanduser("~/.tgpt/api")
        self.api_key = None
        
    def get_api_key(self):
        """
        Retrieves the API key from the file, if not already cached.
        
        Returns:
            str: The API key.
        """
        if self.api_key is None:
            with open(self.filename, 'r') as f:
                self.api_key = f.read().strip()
        return self.api_key

