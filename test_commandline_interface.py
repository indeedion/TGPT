import unittest
from unittest.mock import MagicMock
from api_key_file import ApiKeyFile
from chat_gpt_client import ChatGPTClient
from commandline_interface import CommandLineInterface

class TestCommandLineInterface(unittest.TestCase):

    def setUp(self):
        api = ApiKeyFile()
        self.api_key = api.get_api_key()
        self.client = ChatGPTClient(self.api_key)

        self.cli = CommandLineInterface(self.client)

    def test_handle_command_set_engine(self):
        # Test setting the engine
        self.cli.handle_command("/set_engine text-curie-001")
        self.assertEqual(self.client.model_engine, "text-curie-001")

    def test_handle_command_invalid_command(self):
        # Test invalid command
        self.assertTrue(self.cli.handle_command("/invalid_command"))

    def test_handle_command_exit(self):
        # Test exiting the CLI
        self.assertFalse(self.cli.handle_command("exit"))

    def test_handle_completion(self):
        # Test completion
        self.client.completions = MagicMock(return_value="Test response")
        response = self.cli.handle_completion("Test prompt")
        self.assertEqual(response, "Test response")
        
if __name__ == '__main__':
    unittest.main()

