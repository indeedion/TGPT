import argparse
from gpt_client import GPTClient
from commandline_interface import CommandLineInterface
from api_key_file import ApiKeyFile


def main():
    # Create an ArgumentParser object to handle command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("question", nargs="?", help="Text query")
    parser.add_argument("-c", "--chat", action="store_true", help="Enter chat mode")
    parser.add_argument("-gi", "--generate-image", metavar="PROMPT", help="Generate an image based on the given text prompt")
    parser.add_argument("-gv", "--generate-variation", metavar="EXISTING_IMAGE_PATH", help="Generate a variation of an existing image. Provide the path to the existing image as an argument.")
    parser.add_argument("-n", "--number", type=int, default=1, help="The number of images to generate or vary. Default is 1.")
    parser.add_argument("-t", "--temperature", metavar="TEMPERATURE", type=float, default=0.7, help="The temperature to use for generation (default: 0.5)")
    parser.add_argument("-m", "--max", type=int, default=100, help="The maximum number of tokens to generate for completions(Default: 100)")
    parser.add_argument("-s", "--size", choices=["small", "medium", "large"], default="medium", help="Image size")
    args = parser.parse_args()

    # Load API key from file
    api_key_file = ApiKeyFile()
    api_key = api_key_file.get_api_key()

    # Create client and command line interface objects
    client = GPTClient(api_key, "gpt-3.5-turbo")
    cli = CommandLineInterface(client)

    # Check if a question was provided as an argument
    if args.question:
        print("Sending query...")
        response = cli.handle_completion(args.question, n=args.number, temperature=args.temperature, max_tokens=args.max)

    # Check if chat mode was specified
    elif args.chat:
        cli.run()

    # Check if generate image mode was specified
    elif args.generate_image:
        print("Generating image...")
        image_data = cli.generate_image(args.generate_image, n=args.number, size=args.size)

    # Check if generate variation mode was specified
    elif args.generate_variation:
        print("Creating image variation...")
        image_path = args.generate_variation
        image_data = cli.generate_variation(image_path, n=args.number, size=args.size)

    # Print help message if no arguments are provided
    else:
        parser.print_help()


if __name__ == "__main__":
    main()


