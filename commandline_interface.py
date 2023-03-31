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

        # Extract response from completion
        response = ""
        for choice in completion["choices"]:
            response += choice["message"]

        return response

    def handle_command(self, command):
        if command == "/exit":
            return self._exit()
        elif command.startswith("/set-api-key"):
            return self._set_api_key(command)
        elif command.startswith("/set-model"):
            return self._set_model(command)
        elif command.startswith("/get-models"):
            return self._get_models()
        elif command == "/help":
            return self._print_help()
        else:
            print("Invalid command, please use one of the following:")
            return self._print_help()

    def _exit(self):
        print("Goodbye!")
        sys.exit()

    def _set_api_key(self, api_key):
        self.client.set_api_key(api_key)
        print("API key set.")

    def _set_model(self, model):
        self.client.set_model(model)
        print("Model set.")

    def _get_models(self):
        models = self.client.list_models()
        for model in models["data"]:
            print(f"{model['id']}: {model['display_name']}")

    def _print_help(self):
        print("Available commands:")
        print("exit: Exit the program")
        print("set-api-key [API_KEY]: Set the OpenAI API key")
        print("set-model [MODEL]: Set the GPT model to use")
        print("get-models: List available GPT models")
        print("help: Show this help message")
        print("chat: Enter chat mode")

    def _handle_chat(self):
        print("Entering chat mode. Press Ctrl+C to exit.")
        while True:
            try:
                message = input("You: ")
                if not message:
                    continue
                self.chat_history.append(("user", message))
                response = self.client.chat(message)
                self.chat_history.append(("AI", response))
                print(f"AI: {response}")
            except KeyboardInterrupt:
                print("\nExiting chat mode.")
                return

