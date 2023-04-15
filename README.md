# TGPT

TGPT is a command-line tool for interacting with OpenAI's GPT-3.5-turbo model and generating images using DALL-E. This tool allows users to generate text completions and create images or variations of existing images using text prompts.

### Table of Contents

- [Installation](#installation)
- [Usage](#usage)
   - [Text Completions](#text-completions)
   - [Image Generation](#image-generation)
   - [Image Variation](#image-variation)
- [Classes Overview](#classes-overview)
   - [ConfigHandler](#confighandler)
   - [CommandLineInterface](#commandlineinterface)
   - [GPTClient](#gptclient)
   - [ImageHandler](#imagehandler)
- [Additional Features and Options](#additional-features-and-options)
   - [Chat Mode](#chat-mode)
   - [Customizing Text Completions](#customizing-text-completions)
   - [Customizing Image Generation and Variation](#customizing-image-generation-and-variation)
- [Contributors](#contributors)
- [Contributing](#contributing)
- [License](#license)
- [Changelog](#changelog)
   - [New Features and Improvements](#new-features-and-improvements)
   - [Removals and Deprecations](#removals-and-deprecations)

### Installation

1. Install the package using pip:

```bash
pip install tgpt
```
### Usage

#### Text Completions
To generate text completions, you can run TGPT with your text prompt as an argument:

```bash
tgpt "Your text prompt here"
```

#### Image Generation
To generate an image based on a text prompt, use the gi command followed by the text prompt:

```bash
tgpt gi "A futuristic city skyline"
```

#### Image Variation
To generate a variation of an existing image, use the gv command followed by the path to the image:

```bash
tgpt gv "/path/to/your/image.png"
```

### Classes Overview

##### ConfigHandler 
Handles the retrieval of the API key, model, image path, max tokens, and temperature from the configuration file.

##### CommandLineInterface 
Provides a command-line interface for interacting with the GPTClient and ImageHandler classes. It allows users to generate text completions, images, and image variations.

##### GPTClient 
Responsible for making requests to OpenAI's API. It handles text completions and communicates with the ImageHandler for image-related tasks.

##### ImageHandler 
Manages image generation and variation requests to the DALL-E API. It provides functions to generate images based on text prompts and create variations of existing images.

### Additional Features and Options

##### Chat Mode

To enter chat mode, use the --chat flag:
```bash
tgpt --chat
```

In chat mode, you can have a conversation with the AI by typing your messages in the terminal. Type /exit or /quit to end the session, /help for more commands.

##### Customizing Text Completions

You can customize the text completions by setting the -t, -n, and -m options:
```bash
tgpt tx "Your text prompt here" -t 0.5 -n 3 -m 50
```

-t or --temp: Controls the randomness of the AI's output (default: 0.7).
-n or --num: The number of completions to generate (default: 1).
-m or --max: The maximum number of tokens to generate for completions (default: 100).

##### Customizing Image Generation and Variation

You can customize the image generation and variation by setting the -s and -n options:
```bash
tgpt gi "A futuristic city skyline" -s large -n 3
```
-s or --size: The size of the generated images (options: small, medium, large; default: medium).
-n or --num: The number of images to generate or vary (default: 1).


### Contributors

    Magnus Jansson: mengus00@gmail.com
    GPT-4: openai.com

### Contributing

Contributions are welcome! Please submit a pull request or create an issue to propose changes or report bugs.

### License

GNU General Public License v3.0

### Changelog

##### New Features and Improvements

    - Restructured the project into a Python package for easy installation and distribution.
    - Added the ConfigHandler class for managing configuration, including API key, model, image path, max tokens, and temperature.
    - Replaced the old API key retrieval method with the ConfigHandler class.
    - Deprecated the install.sh script and the tgpt script. Users should use pip to install the package.
    - Enhanced the command-line interface with new options and arguments for greater flexibility and control.

##### Removals and Deprecations

    - Removed the install.sh script as it is now replaced by the package installation using pip.
    - Removed the combine_files.py script and the tgpt file, as the package structure replaces the need for combining files.
    - Deprecated the manual installation instructions for the tgpt script. Users should use pip to install the package.
    - Removed the old image save path configuration method. The image save path is now part of the configuration managed by ConfigHandler.