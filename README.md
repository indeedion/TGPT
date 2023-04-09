# TerminalGPT

TerminalGPT is a command-line tool for interacting with OpenAI's GPT-3.5-turbo model and the DALL-E image generation API. This tool allows users to generate text completions and create images or variations of existing images using text prompts. The tool is written for Linux and currently will not work in other environments.

### Table of Contents

- Usage
   - Text Completions
   - Image Generation
   - Image Variation
- Classes Overview
   - ConfigHandler
   - CommandLineInterface
   - GPTClient
   - ImageHandler

### Installation

   1. Clone the repository to your local machine.
   2. Make sure you have Python 3.6 or later installed.
   3. Run the install script with ```sudo: sudo ./install.sh.``` This script will guide you through the configuration process, including entering your API key and setting the image save path.

### Usage

**Text Completions**
To generate text completions, you can run TerminalGPT with your text prompt as an argument:

```bash

tgpt "Your text prompt here"
```
**Image Generation**
To generate an image based on a text prompt, use the --generate-image flag followed by the text prompt:

```bash

tgpt --generate-image "A futuristic city skyline"
```
**Image Variation**
To generate a variation of an existing image, use the --generate-variation flag followed by the path to the image:

```bash

tgpt --generate-variation "/path/to/your/image.png"
```
If you ran the installation script, a file called tgpt will have been added to your /usr/bin/. Therefore, you can run the application systemwide. If you ran the installation script but do not want it to be executable systemwide, you can remove this file like so:
```bash
sudo rm -f /usr/bin/tgpt
```
You can the copy the tgpt file from the project folder to wherever you like. You can also just run the main.py file form the project folder with ```python main.py```

### Classes Overview

**ConfigHandler** handles the retrieval of the API key, model, image path, max tokens, and temperature from the configuration file.

**CommandLineInterface** provides a command-line interface for interacting with the GPTClient and ImageHandler classes. It allows users to generate text completions, images, and image variations.

**GPTClient** is responsible for making requests to OpenAI's API. It handles text completions and communicates with the ImageHandler for image-related tasks.

**ImageHandler** manages image generation and variation requests to the DALL-E API. It provides functions to generate images based on text prompts and create variations of existing images.

### Additional Features and Options

**Chat Mode**

To enter chat mode, use the --chat flag:

```bash

tgpt --chat
```
In chat mode, you can have a conversation with the AI by typing your messages in the terminal. Type /exit or /quit to end the session.

**Customizing Text Completions**

You can customize the text completions by setting the --temperature, --number, and --max options:

```bash

tgpt "Your text prompt here" --temperature 0.5 --number 3 --max 50
```
    --temperature: Controls the randomness of the AI's output (default: 0.7).
    --number: The number of completions to generate (default: 1).
    --max: The maximum number of tokens to generate for completions (default: 100).

**Customizing Image Generation and Variation**

You can customize the image generation and variation by setting the --size and --number options:

```bash

tgpt --generate-image "A futuristic city skyline" --size large --number 3
```
    --size: The size of the generated images (options: small, medium, large; default: medium).
    --number: The number of images to generate or vary (default: 1).

### Contributors

- Indeedion :mengus00@gmail.com
- GPT-4: openai.com

### Contributing

Contributions are welcome! Please submit a pull request or create an issue to propose changes or report bugs.

### License

GNU General Public License v3.0

### Changelog
**New Features and Improvements**

   - Added the ConfigHandler class for managing configuration, including API key, model, image path, max tokens, and temperature.
   - Replaced the old API key retrieval method with the ConfigHandler class.
   - Added an installation script (install_script.sh) to guide users through the configuration process and copy the tgpt script to /usr/bin/.
   - Updated the tgpt script to include all the necessary code from the Python files for easier installation and removal.
   - Enhanced the command-line interface with new options and arguments for greater flexibility and control.

**Removals and Deprecations**

   - Removed the ApiKeyFile class as it is now replaced by the ConfigHandler class.
   - Deprecated the manual installation instructions for the tgpt script. Users should use the install.sh script for installation.
   - Removed the old image save path configuration method. The image save path is now part of the configuration managed by ConfigHandler.
