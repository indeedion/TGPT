import os
from configparser import ConfigParser


class ConfigHandler:
    def __init__(self):
        self.config = ConfigParser()
        self.config_file_path = os.path.expanduser("~/.tgpt/config")

        if not os.path.exists(self.config_file_path):
            self._create_default_config()
        else:
            self.config.read(self.config_file_path)

    def _create_default_config(self):
        self.config["DEFAULT"] = {
            "API": "",
            "MODEL": "gpt-3.5-turbo",
            "IMAGE_PATH": "~/Pictures/TerminalGPT",
            "MAX_TOKENS": 100,
            "TEMPERATURE": 0.7,
        }

        os.makedirs(os.path.dirname(self.config_file_path), exist_ok=True)

        with open(self.config_file_path, "w") as config_file:
            self.config.write(config_file)
            print(f"Created a new config file at: {self.config_file_path}")

    def get_api_key(self):
        return self.config.get("DEFAULT", "API")

    def get_model(self):
        return self.config.get("DEFAULT", "MODEL")

    def get_image_path(self):
        return self.config.get("DEFAULT", "IMAGE_PATH")

    def get_max_tokens(self):
        return self.config.getint("DEFAULT", "MAX_TOKENS")

    def get_temperature(self):
        return self.config.getfloat("DEFAULT", "TEMPERATURE")
    
if __name__ == "__main__":
    config = ConfigHandler()
    api_key = config.get_api_key()
    model = config.get_model()

