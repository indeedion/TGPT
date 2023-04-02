#!/bin/python

import argparse
from chat_gpt_client import ChatGPTClient
from commandline_interface import CommandLineInterface
from api_key_file import ApiKeyFile

def main():
    # Create an ArgumentParser object to handle command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("question", nargs="?", help="The question to ask ChatGPT")
    parser.add_argument("-c", "--chat", action="store_true", help="Enter chat mode")
    args = parser.parse_args()

    # Load API key from file
    api_key_file = ApiKeyFile()
    api_key = api_key_file.get_api_key()

    # Create client and command line interface objects
    client = ChatGPTClient(api_key, "gpt-3.5-turbo", "https://api.openai.com/v1/chat/completions")
    cli = CommandLineInterface(client)

    # Check if a question was provided as an argument
    if args.question:
        response = cli.handle_completion(args.question)
        cli.print_response(response)
    # Check if chat mode was specified
    elif args.chat:
        cli.run()
    # Print help message if no arguments are provided
    else:
        parser.print_help()

if __name__ == "__main__":
    main()

