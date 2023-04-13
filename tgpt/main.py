import argparse
from .gpt_client import GPTClient
from .commandline_interface import CommandLineInterface
from .config_handler import ConfigHandler

class CustomArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        self.print_help()
        print("\nError: {}\n".format(message))
        self.exit()

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
    parser = CustomArgumentParser(
        description="A command-line interface to interact with OpenAI GPT-3 and generate images based on prompts or variations.",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    subparsers = parser.add_subparsers(dest="subparser_name", title="subcommands", metavar="{tx, gi, gv}")

    # Add subparser for text query
    parser_tx = subparsers.add_parser("tx", help="Send a text query to GPT-3")
    parser_tx.add_argument("question", help="Text query")
    parser_tx.add_argument("-m", "--max", type=int, default=tokens, help=f"The maximum number of tokens to generate for completions(Default: {tokens})")
    parser_tx.add_argument("-n", "--number", type=int, default=1, help="The number of text completions to generate. Default is 1.")
    parser_tx.add_argument("-t", "--temperature", metavar="TEMPERATURE", type=float, default=temperature, help=f"The temperature to use for generation (default: {temperature})")

    # Add subparser for generate image
    parser_gi = subparsers.add_parser("gi", help="Generate an image based on the given text prompt")
    parser_gi.add_argument("prompt", help="Text prompt for generating an image")
    parser_gi.add_argument("-n", "--number", type=int, default=1, help="The number of images to generate. Default is 1.")
    parser_gi.add_argument("-m", "--max", type=int, default=tokens, help=f"The maximum number of tokens to generate for completions(Default: {tokens})")
    parser_gi.add_argument("-s", "--size", choices=["small", "medium", "large"], default="medium", help="Image size")
    parser_gi.add_argument("save_path", nargs='?', default=None, help="The path to save generated images. Optional.")

    # Add subparser for generate variation
    parser_gv = subparsers.add_parser("gv", help="Generate a variation of an existing image")
    parser_gv.add_argument("image_name", help="Name of an existing image")
    parser_gv.add_argument("-n", "--number", type=int, default=1, help="The number of image variations to generate. Default is 1.")
    parser_gv.add_argument("-m", "--max", type=int, default=tokens, help=f"The maximum number of tokens to generate for completions(Default: {tokens})")
    parser_gv.add_argument("-s", "--size", choices=["small", "medium", "large"], default="medium", help="Image size")
    parser_gv.add_argument("save_path", nargs='?', default=None, help="The path to save generated images. Optional.")


    # Add top-level options
    parser.add_argument("-c", "--chat", action="store_true", help="Enter chat mode")
    

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
    if args.subparser_name in ["gi", "gv"] and args.size != image_size:
        image_size = args.size
    
    # Check if a question was provided as an argument
    try:
        # Check if query was provided with subcommand
        if args.subparser_name == "tx":
            print("Sending query...")
            cli.handle_completion(args.question, n=number)

        # Check if chat mode was specified
        elif args.chat:
            cli.run()

        # Check if generate image mode was specified
        elif args.subparser_name == "gi":
            print("Generating image...")
            cli.generate_image(args.prompt, n=number, size=image_size, save_path=args.save_path)

        # Check if generate variation mode was specified
        elif args.subparser_name == "gv":
            print("Creating image variation...")
            image_name = args.existing_image_name
            cli.generate_variation(image_name, n=number, size=image_size, save_path=args.save_path)

        # Print help message if no arguments are provided
        else:
            parser.print_help()

    except Exception as e:
        print(f"Error handling command line arguments or processing request: {e}")


if __name__ == "__main__":
    main()
