import os
import textwrap
from configparser import ConfigParser


class ConfigHandler:
    """
    A configuration handler for TGPT that reads and writes configuration settings.
    
    Attributes:
        config (ConfigParser): A ConfigParser instance for managing the configuration.
        config_file_path (str): The path to the configuration file.
    """
    def __init__(self):
        """
        Initialize the ConfigHandler and read the configuration file or create a default one.
        """
        self.config = ConfigParser()
        self.config_file_path = os.path.expanduser("~/.tgpt/config")

        if not os.path.exists(self.config_file_path):
            self._create_default_config()
        else:
            try:
                self.config.read(self.config_file_path)
            except Exception as e:
                print(f"Error reading config file: {e}")
                self._create_default_config()

    def _create_default_config(self):
        """
        Create a default configuration file and prompt the user for their API key.
        """
        try:
            print(textwrap.dedent("""
                     Welcome to TGPT!
                     Since this is your first time you will need to provide your OpenAI API key.
                     The key can later be found, in ~/.tgpt/config, along wth other settings.
                  """))
            api_key = input("Please enter your API key: ")

            self.config["DEFAULT"] = {
                "API": api_key,
                "MODEL": "gpt-3.5-turbo",
                "MAX_TOKENS": 150,
                "TEMPERATURE": 0.7,
                "WIDTH": 80,
                "NUMBER": 1,
                "IMAGE_SIZE": "medium"
            }

            os.makedirs(os.path.dirname(self.config_file_path), exist_ok=True)

            with open(self.config_file_path, "w") as config_file:
                self.config.write(config_file)
                print(f"Created a new config file at: {self.config_file_path}")
        except Exception as e:
            print(f"Error creating default config file: {e}")

    def get_api_key(self):
        """
        Retrieve the API key from the configuration file.
        
        Returns:
            str: The API key.
        """
        return self.config.get("DEFAULT", "API", fallback="")

    def get_model(self):
        """
        Retrieve the model name from the configuration file.
        
        Returns:
            str: The model name.
        """
        return self.config.get("DEFAULT", "MODEL", fallback="gpt-3.5-turbo")

    def get_max_tokens(self):
        """
        Retrieve the maximum tokens value from the configuration file.
        
        Returns:
            int: The maximum tokens value.
        """
        return self.config.getint("DEFAULT", "MAX_TOKENS", fallback=100)

    def get_temperature(self):
        """
        Retrieve the temperature value from the configuration file.
        
        Returns:
            float: The temperature value.
        """
        return self.config.getfloat("DEFAULT", "TEMPERATURE", fallback=0.7)
    
    def get_width(self):
        """
        Retrieve the width value from the configuration file.
        
        Returns:
            int: The width value.
        """
        return self.config.getint("DEFAULT", "WIDTH", fallback=80)
    
    def get_number(self):
        """
        Retrieve the number value from the configuration file.
        
        Returns:
            int: The number value.
        """
        return self.config.getint("DEFAULT", "NUMBER", fallback=1)

    def get_image_size(self):
        """
        Retrieve the image size value from the configuration file.
        
        Returns:
            str: The image size value.
        """
        return self.config.get("DEFAULT", "IMAGE_SIZE", fallback="medium")


if __name__ == "__main__":
    try:
        config = ConfigHandler()
        api_key = config.get_api_key()
        model = config.get_model()
    except Exception as e:
        print(f"Error initializing ConfigHandler: {e}")
