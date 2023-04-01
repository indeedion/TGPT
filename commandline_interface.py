import sys
from api_key_file import ApiKeyFile

class CommandLineInterface:
    def __init__(self, client):
        self.client = client

    def run(self):
        """Starts the command line interface in chat mode."""
        print("Welcome to ChatGPT!")
        print("Type 'exit' to end the session.")

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
        print(f"\ngpt: {response_text}")

    def handle_completion(self, prompt):
        """
        Handle a single GPT-3 completion request.

        :param prompt: The user's prompt.
        :return: The response text from the GPT-3 model.
        """
        if not prompt:
            return ""

        # Generate chat completion
        completion = self.client.completions(prompt, max_tokens=1024, n=1, stop=None)

        return completion

    def handle_command(self, command):
        if command == "/exit" or command == "/quit":
            return self._exit()
        elif command == "/help":
            self._print_help()
            return True
        else:
            print("Invalid command, please use one of the following:")
            return self._print_help()

    def _exit(self):
        print("Goodbye!")
        sys.exit()

    def _print_help(self):
        print("Available commands:")
        print("/exit or /quit: Exit the program")
        print("/help: Show this help message")

    

