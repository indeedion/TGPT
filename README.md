# TerminalGPT

TerminalGPT is an interactive command-line interface that uses OpenAI's GPT-3 language model to answer questions and engage in conversations with users. It is designed for Linux environments.
And since you're bound to wonder, yes, ChatGPT wrote a lot of this code :)

### Features
- Ability to ask and receive answers to a wide range of questions
- Option to engage in conversations with the model by entering chat mode
- Chat history saved for reference in chat mode
- Support for multiple GPT-3 models
- Clear and user-friendly interface

### Usage

1. Clone this repository to your local machine.
2. Create an account on the OpenAI website and obtain an API key.
3. Create a folder called .tgpt in your home directory.
4. Create a file called api inside the .tgpt folder.
5. Paste your OpenAI API key in the api file and save it.
6. Open a terminal and navigate to the root directory of the cloned repository.
7. Run the following command to start the application: python main.py.
8. Follow the prompts to ask questions or enter chat mode.
9. (optional) put the gpt file in any folder in your path, and run with "gpt" from anywhere.

### Classes
The TerminalGPT project is made up of the following classes:
- ChatGPTClient: This class contains the methods used to interface with the OpenAI API and obtain responses from the language model.
- CommandLineInterface: This class handles user input and output for the command-line interface, including the ability to enter chat mode and display chat history.
- Main: This class ties together the ChatGPTClient and CommandLineInterface classes and serves as the entry point for the application.

### Requirements
- Python 3.7 or higher
- The openai and requests modules for Python
- An OpenAI API key

### Known Issues
None at the moment.

### Contributors
indeedion

### License
GNU General Public License v3.0
