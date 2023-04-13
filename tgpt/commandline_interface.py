import sys
import textwrap
from .gpt_client import GPTClient


class CommandLineInterface:
    def __init__(self, client):
        self.client = client
        self.width = 80

    def run(self):
        print(f"Welcome to TGPT! You are talking to model: {self.client.get_model()}")
        print("Type '/exit or /quit' to end the session, /help for more commands.")

        while True:
            try:
                user_input = input("\nYou: ")
                if user_input.strip() == "":
                    continue
                if user_input.startswith("/"):
                    command_parts = user_input.split()
                    command = command_parts[0]
                    args = command_parts[1:]
                    if not self.handle_command(command, args):
                        break
                else:
                    response = self.client.completion(user_input)
                    wrapped_lines = []
                    lines = response[0].split("\n")
                    for line in lines:
                        wrapped_line = textwrap.fill(line, width=self.width)
                        wrapped_lines.append(wrapped_line)

                    wrapped_completion = "\n".join(wrapped_lines)
                    print(f"\nGPT: {wrapped_completion}") 
            except Exception as e:
                print(f"An error occurred: {e}")

    def handle_completion(self, prompt, n=1):
        if not prompt:
            return ""

        response = self.client.completion(prompt, n=n, stop=None)

        if not isinstance(response, list):
            response = [response]

        for i, completion in enumerate(response):
            if n > 1:
                print(f"\nAnswer {i + 1}:")
            else:
                print("\nAnswer:")
            wrapped_lines = []
            lines = completion.split("\n")
            for line in lines:
                wrapped_line = textwrap.fill(line, width=self.width)
                wrapped_lines.append(wrapped_line)

            wrapped_completion = "\n".join(wrapped_lines)
            print(f"\n{wrapped_completion}")

        return True


    def handle_command(self, command, args=None):
        if command in ("/exit", "/quit"):
            sys.exit(print("Goodbye!"))
        elif command == "/help":
            self._print_help()
            return True
        elif command == "/temperature":
            if args and len(args) > 0:
                temp = float(args[0])
            else:
                temp = float(input("New temperature: "))
            self.client.set_temperature(temp)
            print(f"Temperature set to {temp}")
            return True
        elif command == "/max-tokens":
            if args and len(args) > 0:
                tokens = int(args[0])
            else:
                tokens = int(input("New max tokens: "))
            self.client.set_max_tokens(tokens)
            print(f"Max tokens set to {tokens}")
            return True
        elif command == "/width":
            if args and len(args) > 0:
                width = int(args[0])
            else:
                width = int(input("New width: "))
            self.set_width(width)
            print(f"New width set to {width} ")
            return True
        else:
            print("Invalid command, please use one of the following:")
            self._print_help()
            return True

    def generate_image(self, prompt, n=1, size="medium", response_format="url", save_path = None):
        self.client.generate_image(prompt=prompt, n=n, size=size, response_format=response_format, save_path = save_path)
        return True

    def generate_variation(self, image_name, size="medium", n=1, response_format="url", save_path = None):
        self.client.generate_variation(image_name, size=size, n=n, response_format=response_format, save_path = save_path)
        return True

    def set_width(self, width):
        self.width = width

    def _print_help(self):
        print("Available commands:")
        print("/exit or /quit: Exit the program")
        print("/temperature: set new temperature")
        print("/max-tokens: set new max tokens")
        print("/width: set new print width")
        print("/help: Show this help message")


if __name__ == "__main__":
    try:
        client = GPTClient(api_key="API_KEY")
        cli = CommandLineInterface(client)
        cli.run()
    except Exception as e:
        print(f"An error occurred during initialization: {e}")
