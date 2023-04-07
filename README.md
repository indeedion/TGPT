# TerminalGPT

TerminalGPT is a command-line tool for interacting with OpenAI's GPT-3.5-turbo model and the DALL-E image generation API. This tool allows users to generate text completions and create images or variations of existing images using text prompts. The tool is written for Linux and currently will not work in other environments.

### Table of Contents
- Installation
   - Usage
      - Text Completions
      - Image Generation
      - Image Variation
   - Classes Overview
       - ApiKeyFile
       - CommandLineInterface
       - GPTClient
       - ImageHandler

### Installation

   1. Clone the repository to your local machine.
   2. Make sure you have Python 3.6 or later installed.
   3. Place your OpenAI API key in a file located at ~/.tgpt/api.
  
### Optional Installation steps for better usage
   4. Copy the file named tgpt to /usr/bin folder for easier systemwide usage.
      Go to the folder you cloned it to
      ```bash
      cd /path/you/cloned/it/to/terminalGPT
      ```
      Make sure this file is executable
      ```bash
      sudo chmod +x tgpt
      ```
      Then copy
      ```bash
      sudo cp tgpt /usr/bin/
      ```
      This file contains all code in one file for easier usage.
      Now you can use it from anywhere like this
      ```bash
      tgpt --chat
      ```

### Usage
Text Completions:
To generate text completions, you can run the TerminalGPT script with your text prompt as an argument:

```bash

python main.py "Your text prompt here"

```
Image Generation:
To generate an image based on a text prompt, use the --generate-image flag followed by the text prompt:

```bash

python main.py --generate-image "A futuristic city skyline"

```
Image Variation:
To generate a variation of an existing image, use the --generate-variation flag followed by the path to the image:

```bash

python main.py --generate-variation "/path/to/your/image.png"

```
**Please note** that images will be saved to ~/Pictures/TerminalGPT/. You may have to create this folder if it does not allready exist.

### Classes Overview
**ApiKeyFile** handles the retrieval of the API key from a file. It stores the API key in memory to avoid reading the file multiple times.
CommandLineInterface

**CommandLineInterface** provides a command-line interface for interacting with the GPTClient and ImageHandler classes. It allows users to generate text completions, images, and image variations.

**GPTClient** is responsible for making requests to OpenAI's API. It handles text completions and communicates with the ImageHandler for image-related tasks.

**ImageHandler** manages image generation and variation requests to the DALL-E API. It provides functions to generate images based on text prompts and create variations of existing images.

### Additional Features and Options
Chat Mode

To enter chat mode, use the --chat flag:

```bash

python main.py --chat

```
In chat mode, you can have a conversation with the AI by typing your messages in the terminal. Type /exit or /quit to end the session.
Customizing Text Completions

You can customize the text completions by setting the --temperature, --number, and --max options:

```bash

python main.py "Your text prompt here" --temperature 0.5 --number 3 --max 50

```
    --temperature: Controls the randomness of the AI's output (default: 0.7).
    --number: The number of completions to generate (default: 1).
    --max: The maximum number of tokens to generate for completions (default: 100).

### Customizing Image Generation and Variation

You can customize the image generation and variation by setting the --size and --number options:

```bash

python main.py --generate-image "A futuristic city skyline" --size large --number 3

```
    --size: The size of the generated images (options: small, medium, large; default: medium).
    --number: The number of images to generate or vary (default: 1).
    
### Contributors
Indeedion :mengus00@gmail.com

### Contributing

Contributions are welcome! Please submit a pull request or create an issue to propose changes or report bugs.

### License

GNU General Public License v3.0
