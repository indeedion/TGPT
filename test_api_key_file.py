import unittest
from api_key_file import ApiKeyFile

class TestApiKeyFile(unittest.TestCase):
    def test_get_api_key(self):
        filename = "test_api_key_file.txt"
        with open(filename, "w") as f:
            f.write("test_api_key")

        api_key_file = ApiKeyFile(filename)
        self.assertEqual(api_key_file.get_api_key(), "test_api_key")

        with open(filename, "w") as f:
            f.write("new_api_key")

        self.assertEqual(api_key_file.get_api_key(), "test_api_key")

        api_key_file.api_key = None
        self.assertEqual(api_key_file.get_api_key(), "new_api_key")

        # clean up file
        import os
        os.remove(filename)

if __name__ == '__main__':
    unittest.main()

