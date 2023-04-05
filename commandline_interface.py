import sys
import os
import requests
import urllib.request
from api_key_file import ApiKeyFile
from datetime import datetime

class CommandLineInterface:
    """
    This class provides a command line interface for interacting with a GPT-3 model.
    
    Attributes:
        client (obj): The GPT-3 API client instance.
    """

    def __init__(self, client):
        """
        Initializes the CommandLineInterface instance with the provided GPT-3 API client.
        
        :param client: The GPT-3 API client instance.
        """
        self.client = client

    def run(self):
        """
        Starts the command line interface in chat mode.
        """
        print("Welcome to TerminalGPT!")
        print("Type '/exit or /quit' to end the session.")

        while True:
            user_input = input("\nYou: ")
            if user_input.strip() == "":
                continue
            if user_input.startswith("/"):
                if not self.handle_command(user_input):
                    break
            else:
                response = self.client.generate_text(user_input)
                self.print_response(response)

    def print_response(self, response_text):
        """
        Prints the GPT-3 model response.
        
        :param response_text: The response text from the GPT-3 model.
        """
        print(f"\ngpt: {response_text}")

    def handle_completion(self, prompt, n=1, t=0.7, m=1024):
        """
        Handle a single GPT-3 completion request.

        :param prompt: The user's prompt.
        :return: The response text from the GPT-3 model.
        """
        if not prompt:
            return ""

        # Generate chat completion
        response = self.client.completions(prompt, n=n, t=t, m=m, stop=None)
        for i, completion in enumerate(response):
            print(f"\nAnswer {i+1}:")
            print(f"\n{completion}")
        print("\n")

        return True

    def handle_command(self, command):
        """
        Processes user commands and returns a boolean indicating whether to continue the chat session.
        
        :param command: The user's command.
        :return: True if the chat session should continue, False otherwise.
        """
        if command == "/exit" or command == "/quit":
            return self._exit()
        elif command == "/help":
            self._print_help()
            return True
        elif command.startswith("/generate_image"):
            command_parts = command.split(" ")
            if len(command_parts) < 2:
                print("Invalid command, please specify a prompt.")
                return True
            prompt = " ".join(command_parts[1:])
            image_data = self.client.generate_image(prompt)
            if image_data:
                self.save_image(image_data, "generated_image.png")
                print("Image generated and saved to generated_image.png")
            else:
                print("Failed to generate image.")
            return True
        elif command.startswith("/generate_edit"):
            command_parts = command.split(" ")
            if len(command_parts) < 4:
                print("Invalid command, please specify an image path, mask path, and prompt.")
                return True
            image_path = command_parts[1]
            mask_path = command_parts[2]
            prompt = " ".join(command_parts[3:])
            image_data = self.client.generate_edit(image_path, mask_path, prompt)
            if image_data:
                self.save_image(image_data, "edited_image.png")
                print("Image edited and saved to edited_image.png")
            else:
                print("Failed to edit image.")
            return True
        elif command.startswith("/generate_variation"):
            command_parts = command.split(" ")
            if len(command_parts) < 2:
                print("Invalid command, please specify an image path.")
                return True
            image_path = command_parts[1]
            image_data = self.client.generate_variation(image_path)
            if image_data:
                self.save_image(image_data, "generated_variation.png")
                print("Image variation generated and saved to generated_variation.png")
            else:
                print("Failed to generate image variation.")
            return True
        elif command.startswith("/save_image"):
            command_parts = command.split(" ")
            if len(command_parts) < 3:
                print("Invalid command, please specify an image URL and file path.")
                return True
            url = command_parts[1]
            path = command_parts[2]
            self.client.save_image(url, path)
            print(f"Image saved to {path}")
            return True
        elif command == "/temperature":
            temp = float(input("New temperature: "))
            self.client.temperature = temp
            print(f"Temperature set to {temp}")
            return True
        elif command == "/max-tokens":
            tokens = int(input("New max tokens: "))
            self.client.max_tokens = tokens
            print(f"Max tokens set to {tokens}")
            return True
        else:
            print("Invalid command, please use one of the following:")
            return self._print_help()

    def generate_image(self, prompt, n=1, size="512x512", response_format="url"):
        """
        Generates an image based on the provided text prompt and returns the image data.

        :param prompt: The text prompt to generate the image from.
        :param n: The number of images to generate (default 1).
        :param size: The size of the generated image (default "512x512").
        :param response_format: The format of the image data to return (default "url").
        :return: The image data in the specified format.
        """
        response = self.client.generate_image(prompt=prompt, n=n, size=size, response_format=response_format)

        now = datetime.now()
        timestamp = now.strftime("%Y:%m:%d-%H:%M:%S")

        for i, image_url in enumerate(response):
            self.save_image(image_url, os.path.expanduser(f"~/Pictures/TerminalGPT/gpt-generate-{i}-{timestamp}.png"))

        #image_data = self.client.get_image_data(response[0]['url'])
        return True

    def generate_variation(self, image_path, size="512x512", n=1, response_format="url"):
        """
        Generates a variation of an existing image given an image file path, size, and number of images to generate.

        :param image_path: The path to the image file.
        :param size: The size of the generated image (default "512x512").
        :param n: The number of images to generate (default 1).
        :param response_format: The format of the image data to return (default "url").
        :return: The image data in the specified format.
        """

        response = self.client.generate_variation(image_path=image_path, size=size, n=n, response_format=response_format)

        now = datetime.now()
        timestamp = now.strftime("%Y:%m:%d-%H:%M:%S")

        for i, image_url in enumerate(response):
            self.save_image(image_url, os.path.expanduser(f"~/Pictures/TerminalGPT/gpt-variation-{i}-{timestamp}.png"))

        return True


    def save_image(self, url, file_path, timeout=30):
        with urllib.request.urlopen(url['url'], timeout=timeout) as response, open(file_path, 'wb') as out_file:
            out_file.write(response.read())
        print(f"Saved image to {file_path}")

    def _exit(self):
        """
        Exits the program and prints a goodbye message.
        """
        print("Goodbye!")
        sys.exit()

    def _print_help(self):
        """
        Prints the help message with the list of available commands.
        """
        print("Available commands:")
        print("/exit or /quit: Exit the program")
        print("/temperature: set new temperature")
        print("/max-tokens: set new max tokens")
        print("/help: Show this help message")
        

    

