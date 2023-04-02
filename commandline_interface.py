import sys
from api_key_file import ApiKeyFile

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
        else:
            print("Invalid command, please use one of the following:")
            return self._print_help()

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
        print("/help: Show this help message")

    

