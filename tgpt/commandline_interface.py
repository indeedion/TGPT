import sys
import textwrap
import threading
import time
from .gpt_client import GPTClient


class CommandLineInterface:
    """
    A command line interface for interacting with a GPTClient instance.
    
    Attributes:
        client (GPTClient): The GPTClient instance for making API calls.
        width (int): The maximum width for text wrapping.
        spinner_active (bool): Flag to control the spinner during API calls.
    """
    def __init__(self, client):
        """
        Initialize the CommandLineInterface with a GPTClient instance.
        
        Args:
            client (GPTClient): The GPTClient instance for making API calls.
        """
        self.client = client
        self.width = 80
        self.spinner_active = False

    def run(self):
        """
        Start the main loop of the command line interface.
        """
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
        """
        Handle completion requests to the GPTClient.
        
        Args:
            prompt (str): The prompt to send to the GPTClient.
            n (int, optional): The number of responses to request. Defaults to 1.
        
        Returns:
            bool: True if a response is received, False otherwise.
        """
        if not prompt:
            return ""

        sys.stdout.write("Sending query... ")
        sys.stdout.flush()

        self.spinner_active = True
        spinner_thread = threading.Thread(target=self.spin_cursor)
        spinner_thread.start()

        response = self.client.completion(prompt, n=n, stop=None)

        self.spinner_active = False
        spinner_thread.join()

        if not isinstance(response, list):
            response = [response]

        for i, completion in enumerate(response):
            wrapped_lines = []
            lines = completion.split("\n")
            for line in lines:
                wrapped_line = textwrap.fill(line, width=self.width)
                wrapped_lines.append(wrapped_line)

            wrapped_completion = "\n".join(wrapped_lines)
            completion_length = len(wrapped_completion)

            if n > 1:
                print(f"\n\nAnswer {i + 1}:")
            elif completion_length > 40:
                print("\n\nAnswer:")

            print(f"\n{wrapped_completion}")

        print("")
        return True


    def handle_command(self, command, args=[]):
        """
        Handle command inputs from the user.
        
        Args:
            command (str): The command inputted by the user.
            args (list, optional): Additional arguments for the command. Defaults to [].
        
        Returns:
            bool: True if the command is handled, False otherwise.
        """
        if command in ("/exit", "/quit"):
            sys.exit(print("Goodbye!"))
        elif command == "/help":
            self._print_help()
            return True
        elif command == "/temperature":
            if len(args) > 0:
                temp = float(args[0])
            else:
                temp = float(input("New temperature: "))
            self.client.set_temperature(temp)
            print(f"Temperature set to {temp}")
            return True
        elif command == "/max-tokens":
            if len(args) > 0:
                tokens = int(args[0])
            else:
                tokens = int(input("New max tokens: "))
            self.client.set_max_tokens(tokens)
            print(f"Max tokens set to {tokens}")
            return True
        elif command == "/width":
            if len(args) > 0:
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

    def generate_image(self, prompt, n=1, size="medium", response_format="url", save_path=None):
        """
        Generate an image using the GPTClient's image generation functionality.
        
        Args:
            prompt (str): The prompt to generate the image.
            n (int, optional): The number of images to generate. Defaults to 1.
            size (str, optional): The size of the generated image. Defaults to "medium".
            response_format (str, optional): The format of the response. Defaults to "url".
            save_path (str, optional): The path to save the generated images. Defaults to None.
        
        Returns:
            list: A list of save paths of the generated images, or False if an error occurs.
        """
        try:
            sys.stdout.write("Generating image... ") 
            sys.stdout.flush() 

            self.spinner_active = True
            spinner_thread = threading.Thread(target=self.spin_cursor)
            spinner_thread.start()

            save_paths = self.client.generate_image(prompt=prompt, n=n, size=size, response_format=response_format, save_path=save_path)

            self.spinner_active = False
            spinner_thread.join()

            print("Image generated successfully.")  

        except Exception as e:
            self.spinner_active = False
            spinner_thread.join()
            print(f"\rError generating image: {e}")
            return False
        return save_paths


    def generate_variation(self, image_name, size="medium", n=1, response_format="url", save_path=None):
        """
        Generate a variation of an image using the GPTClient's image variation functionality.
        
        Args:
            image_name (str): The name of the image to generate a variation for.
            size (str, optional): The size of the generated image. Defaults to "medium".
            n (int, optional): The number of variations to generate. Defaults to 1.
            response_format (str, optional): The format of the response. Defaults to "url".
            save_path (str, optional): The path to save the generated images. Defaults to None.
        
        Returns:
            list: A list of save paths of the generated image variations, or False if an error occurs.
        """
        try:
            sys.stdout.write("Generating image variation... ") 
            sys.stdout.flush()  

            self.spinner_active = True
            spinner_thread = threading.Thread(target=self.spin_cursor)
            spinner_thread.start()

            save_paths = self.client.generate_variation(image_name, size=size, n=n, response_format=response_format, save_path=save_path)

            self.spinner_active = False
            spinner_thread.join()
            print("Image variation created successfully.")
        except Exception as e:
            print(f"Error generating image variation: {e}")
            return False
        return save_paths

    def set_width(self, width):
        """
        Set the width attribute for text wrapping.
        
        Args:
            width (int): The new width for text wrapping.
        """
        self.width = width

    @staticmethod
    def spinning_cursor():
        """
        Generator function for a spinning cursor animation.
        """
        while True:
            for cursor in '|/-\\':
                yield cursor

    def spin_cursor(self):
        """
        Display a spinning cursor animation while the spinner_active flag is True.
        """
        spinner = self.spinning_cursor()
        while self.spinner_active:
            sys.stdout.write(next(spinner))
            sys.stdout.flush()
            time.sleep(0.1)
            sys.stdout.write('\b')

    def _print_help(self):
        """
        Print the help message with available commands.
        """
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
