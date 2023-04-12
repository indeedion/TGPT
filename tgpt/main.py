import argparse
from .gpt_client import GPTClient
from .commandline_interface import CommandLineInterface
from .config_handler import ConfigHandler


def main():
    # Read config file and load values
    try:
        # Read config file and load values
        config = ConfigHandler()
        api_key = config.get_api_key()
        model = config.get_model()
        tokens = config.get_max_tokens()
        temperature = config.get_temperature()
        image_size = config.get_image_size()
        width = config.get_width()
        number = config.get_number()
    except Exception as e:
        print(f"Error loading config values: {e}")
        return

    # Create an ArgumentParser object to handle command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("question", nargs="?", help="Text query")
    parser.add_argument("-c", "--chat", action="store_true", help="Enter chat mode")
    parser.add_argument("-gi", "--generate-image", metavar="PROMPT", help="Generate an image based on the given text prompt")
    parser.add_argument("-gv", "--generate-variation", metavar="EXISTING_IMAGE_NAME", help="Generate a variation of an existing image. Provide the name of an existing image as an argument.")
    parser.add_argument("-n", "--number", type=int, default=1, help="The number of images to generate or vary. Default is 1.")
    parser.add_argument("-t", "--temperature", metavar="TEMPERATURE", type=float, default=temperature, help=f"The temperature to use for generation (default: {temperature})")
    parser.add_argument("-m", "--max", type=int, default=tokens, help=f"The maximum number of tokens to generate for completions(Default: {tokens})")
    parser.add_argument("-s", "--size", choices=["small", "medium", "large"], default="medium", help="Image size")
    try:
        args = parser.parse_args()
    except SystemExit:
        return
    
    # Create client and command line interface objects
    try:
        # Create client and command line interface objects
        client = GPTClient(api_key, model)
        client.set_max_tokens(max_tokens=tokens)
        client.set_temperature(temperature=temperature)
        cli = CommandLineInterface(client)
        cli.set_width(width)
    except Exception as e:
        print(f"Error initializing GPTClient or CommandLineInterface: {e}")
        return
    
    # Set values passed from CLI if present
    if args.max != tokens:
        client.max_tokens = args.max
    if args.temperature != temperature:
        client.temperature = args.temperature
    if args.number != number:
        number = args.number
    if args.size != image_size:
        image_size = args.size
    
    # Check if a question was provided as an argument
    try:
        # Check if a question was provided as an argument
        if args.question:
            print("Sending query...")
            cli.handle_completion(args.question, n=number)

        # Check if chat mode was specified
        elif args.chat:
            cli.run()

        # Check if generate image mode was specified
        elif args.generate_image:
            print("Generating image...")
            cli.generate_image(args.generate_image, n=number, size=image_size)

        # Check if generate variation mode was specified
        elif args.generate_variation:
            print("Creating image variation...")
            image_name = args.generate_variation
            cli.generate_variation(image_name, n=number, size=image_size)

        # Print help message if no arguments are provided
        else:
            parser.print_help()

    except Exception as e:
        print(f"Error handling command line arguments or processing request: {e}")


if __name__ == "__main__":
    main()
