import sys
from api_key_file import ApiKeyFile

class CommandLineInterface:
    def __init__(self, client, history_len=3):
        self.client = client
        self.history = []
        self.history_len = history_len

    def run(self):
        #print("Welcome to the ChatGPT command line interface!")
        while True:
            prompt = self.prompt_for_input()
            if prompt.strip() == "":
                continue
            if prompt.startswith("/"):
                if not self.handle_command(prompt):
                    break
            else:
                response = self.handle_completion(prompt)
                self.print_response(response)

    def print_response(self, response_text):
        print(response_text)

    def prompt_for_input(self):
        # Prompts user for input from the terminal
        return input("> ")

    def handle_completion(self, prompt):
        # Append the prompt to the history
        self.history.append(prompt)

        # Call the client's completion method with the updated history and return the response
        response = self.client.completions(prompt=" ".join(self.history), max_tokens=100)

        # Append the response to the history
        response_text = response[0]["text"].strip()
        self.history.append(response_text)

        return response_text

    def handle_command(self, command):
        # Handles special commands from the user
        if command.startswith("/set_engine"):
            new_engine = command.split()[1]
            self.client.set_engine(new_engine)
            print(f"Engine set to {new_engine}")
            return True
        elif command == "/quit" or command == "/exit":
            #print("Goodbye!")
            return False
        else:
            print(f"Invalid command: {command}")
            return True

