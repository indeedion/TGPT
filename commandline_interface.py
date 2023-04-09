import sys
import os
import urllib.request
from gpt_client import GPTClient
from datetime import datetime


class CommandLineInterface:
    def __init__(self, client):
        self.client = client

    def run(self):
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
                response = self.client.completion(user_input)
                print(response[0])  

    def handle_completion(self, prompt, n=1, temperature=0.7, max_tokens=100):
        if not prompt:
            return ""

        response = self.client.completion(prompt, n=n, temperature=temperature, max_tokens=max_tokens, stop=None)

        if not isinstance(response, list):
            response = [response]

        for i, completion in enumerate(response):
            if i + 1 == 1:
                print("\nAnswer:")
            else:
                print(f"\nAnswer {i+1}:")
            print(f"\n{completion}")
        print("\n")

        return True

    def handle_command(self, command):
        if command in ("/exit", "/quit"):
            sys.exit(print("Goodbye!"))
        elif command == "/help":
            return self._print_help()
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

    def generate_image(self, prompt, image_path, n=1, size="medium", response_format="url"):
        response = self.client.generate_image(prompt=prompt, n=n, size=size, response_format=response_format)
        timestamp = datetime.now().strftime("%Y:%m:%d-%H:%M:%S")

        for i, image_url in enumerate(response):
            self.save_image(image_url, os.path.expanduser(f"{image_path}/gpt-generate-{i}-{timestamp}.png"))

        return True

    def generate_variation(self, image_path, size="medium", n=1, response_format="url"):
        response = self.client.generate_variation(image_path=image_path, size=size, n=n, response_format=response_format)
        timestamp = datetime.now().strftime("%Y:%m:%d-%H:%M:%S")

        output_folder = os.path.dirname(os.path.abspath(image_path))

        for i, image_url in enumerate(response):
            self.save_image(image_url, os.path.join(output_folder, f"gpt-variation-{i}-{timestamp}.png"))

        return True

    def save_image(self, url, file_path, timeout=30):
        with urllib.request.urlopen(url['url'], timeout=timeout) as response, open(file_path, 'wb') as out_file:
            out_file.write(response.read())
        print(f"Saved image to {file_path}")

    def _print_help(self):
        print("Available commands:")
        print("/exit or /quit: Exit the program")
        print("/temperature: set new temperature")
        print("/max-tokens: set new max tokens")
        print("/help: Show this help message")


if __name__ == "__main__":
    client = GPTClient(api_key="API_KEY")
    cli = CommandLineInterface(client)
    cli.run()
