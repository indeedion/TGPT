import os
from configparser import ConfigParser


class ConfigHandler:
    def __init__(self):
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
        try:
            self.config["DEFAULT"] = {
                "API": "",
                "MODEL": "gpt-3.5-turbo",
                "IMAGE_PATH": "~/Pictures/TGPT",
                "MAX_TOKENS": 100,
                "TEMPERATURE": 0.7,
            }

            os.makedirs(os.path.dirname(self.config_file_path), exist_ok=True)

            with open(self.config_file_path, "w") as config_file:
                self.config.write(config_file)
                print(f"Created a new config file at: {self.config_file_path}")
        except Exception as e:
            print(f"Error creating default config file: {e}")

    def get_api_key(self):
        return self.config.get("DEFAULT", "API", fallback="")

    def get_model(self):
        return self.config.get("DEFAULT", "MODEL", fallback="gpt-3.5-turbo")

    def get_image_path(self):
        return self.config.get("DEFAULT", "IMAGE_PATH", fallback="~/Pictures/TGPT")

    def get_max_tokens(self):
        return self.config.getint("DEFAULT", "MAX_TOKENS", fallback=100)

    def get_temperature(self):
        return self.config.getfloat("DEFAULT", "TEMPERATURE", fallback=0.7)

if __name__ == "__main__":
    try:
        config = ConfigHandler()
        api_key = config.get_api_key()
        model = config.get_model()
    except Exception as e:
        print(f"Error initializing ConfigHandler: {e}")
