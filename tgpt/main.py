import argparse
from .gpt_client import GPTClient
from .commandline_interface import CommandLineInterface
from .config_handler import ConfigHandler

class CustomArgumentParser(argparse.ArgumentParser):
    """
    A custom ArgumentParser that overrides the error method to display the help message along with the error message.
    """
    def error(self, message):
        """
        Override the default error method to display the help message along with the error message.
        """
        self.print_help()
        print("\nError: {}\n".format(message))
        self.exit()

def main():
    """
    The main function for the command-line interface to interact with OpenAI's GPT-3.5 API.
    This function handles command-line arguments and calls the appropriate methods based on the input.
    """
    
    # Read config file and load values
    try:
        config = ConfigHandler()
        api_key = config.get_api_key()
        model = config.get_model()
        tokens = config.get_max_tokens()
        temperature = config.get_temperature()
        image_size = config.get_image_size()
        width = config.get_width()
        number = config.get_number()
        client = GPTClient(api_key, model)
        cli = CommandLineInterface(client)
    except Exception as e:
        print(f"Error loading config values, initializing GPTClient or CommandLineInterface: {e}")
        return

    # Create an ArgumentParser object to handle command line arguments
    parser = argparse.ArgumentParser(
        description="A command-line interface to chat with OpenAI GPT-3.5, and generate images based on prompts or variations.\n\n"
                    "To see detailed help for each subcommand, run: tgpt <subcommand> -h\n"
                    "Example: tgpt tx -h\n",
        epilog="",
        formatter_class=argparse.RawTextHelpFormatter,
        add_help=False,
    )
    subparsers = parser.add_subparsers(dest="subparser_name", title="subcommands", metavar="{tx, gi, gv}")

    # Add subparser for text query
    parser_tx = subparsers.add_parser("tx", help="Send a text query to GPT-3.5")
    parser_tx.description = "Query GPT with a question or statement and get an answer"
    parser_tx.usage = "usage: tgpt tx prompt [-h] [-n NUM] [-t TEMP] [-m MAX]"
    parser_tx.add_argument("prompt", type=str, help="Text query to send to GPT-3.5")
    parser_tx.add_argument("-n", "--num", type=int, default=1, help="Number of responses to generate (Default: 1)")
    parser_tx.add_argument("-t", "--temp", type=float, default=temperature, help=f"Sampling temperature for generating responses (Default: {temperature})")
    parser_tx.add_argument("-m", "--max", type=int, default=tokens, help=f"The maximum number of tokens to generate for completions(Default: {tokens})")

    parser_gi = subparsers.add_parser("gi", help="Generate an image based on the given text prompt", formatter_class=argparse.RawDescriptionHelpFormatter)
    parser_gi.description = "Generate images from text prompt"
    parser_gi.usage = "usage: tgpt gi prompt [save_path] [-h] [-s {small,medium,large}] [-n NUM] [-t TEMP]"
    parser_gi.add_argument("prompt", help="The text prompt to generate an image")
    parser_gi.add_argument("save_path", nargs="?", default=None, help="Path to save the generated image (default: current directory)")
    parser_gi.add_argument("-s", "--size", choices=["small", "medium", "large"], default="medium", help=f"The size of the generated image (default: {image_size})")
    parser_gi.add_argument("-n", "--num", type=int, default=1, help="The number of images to generate (default: 1)")
    parser_gi.add_argument("-t", "--temp", type=float, default=temperature, help=f"Sampling temperature for generating responses (Default: {temperature})")

    parser_gv = subparsers.add_parser("gv", help="Generate a variation of an existing image")
    parser_gv.description = "Generate variations of already existing image"
    parser_gv.usage = "usage: tgpt gv image_path [save_path] [-h] [-s {small,medium,large}] [-n NUM] [-t TEMP]"
    parser_gv.add_argument("image_name", type=str, help="Path to the input image for generating a variation")
    parser_gv.add_argument("save_path", type=str, nargs="?", default="", help="Optional save path for the generated images (default: current directory)")
    parser_gv.add_argument("-s", "--size", type=str, choices=["small", "medium", "large"], default="medium", help=f"Size of the generated image (Default: {image_size})")
    parser_gv.add_argument("-n", "--num", type=int, default=1, help="Number of image variations to generate (Default: 1)")
    parser_gv.add_argument("-t", "--temp", type=float, default=temperature, help=f"Sampling temperature for generating responses (Default: {temperature})")
    
    # Add top-level options
    parser.add_argument("-c", "--chat", action="store_true", help="Enter chat mode")
    
    try:
        args = parser.parse_args()
    except SystemExit:
        return
    
    # Set persistent default values to GPTClient and CommandLineInterface
    client.set_max_tokens(tokens)
    client.set_temperature(temperature)
    cli.set_width(width)
    
    
    # Set values passed from CLI if present
    if hasattr(args, 'max') and args.max != tokens:
        client.max_tokens = args.max
    if hasattr(args, 'temperature') and args.temperature != temperature:
        client.temperature = args.temperature
    if hasattr(args, 'num') and args.num != number:
        number = args.num
    if hasattr(args, 'size') and args.size != image_size:
        image_size = args.size
    
    # Check if a question was provided as an argument
    try:
        # Check if query was provided with subcommand
        if args.subparser_name == "tx":
            cli.handle_completion(args.prompt, n=number)

        # Check if chat mode was specified
        elif args.chat:
            cli.run()

        # Check if generate image mode was specified
        elif args.subparser_name == "gi":
            cli.generate_image(args.prompt, n=number, size=image_size, save_path=args.save_path)

        # Check if generate variation mode was specified
        elif args.subparser_name == "gv":
            image_name = args.image_name
            cli.generate_variation(image_name, n=number, size=image_size, save_path=args.save_path)

        # Print help message if no arguments are provided
        else:
            parser.print_help()

    except Exception as e:
        print(f"Error handling command line arguments or processing request: {e}")


if __name__ == "__main__":
    main()
