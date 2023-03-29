import unittest
from api_key_file import ApiKeyFile
from chat_gpt_client import ChatGPTClient

class TestChatGPTClient(unittest.TestCase):
    def setUp(self):
        api = ApiKeyFile("openai")
        self.api_key = api.get_api_key()
        self.client = ChatGPTClient(self.api_key)
    
    def test_prompt(self):
        prompt = "Hello, my name is "
        response = self.client.prompt(prompt, max_tokens=5)
        self.assertTrue(isinstance(response, str))
        
    def test_completions(self):
        prefix = "The quick brown fox"
        response = self.client.completions(prompt=prefix, max_tokens=5)
        self.assertTrue(isinstance(response, list))
        self.assertTrue("text" in response[0].keys())
        self.assertTrue(isinstance(response[0]["text"], str))
        
    def test_get_engine(self):
        expected_engine_id = 'text-davinci-002'
        engine_info = self.client.get_engine()
        engine_id = engine_info['id']
        self.assertEqual(engine_id, expected_engine_id) 

    def test_set_engine(self):
        new_engine = "text-davinci-002"
        self.client.set_engine(new_engine)
        engine = self.client.get_engine()
        self.assertEqual(engine['id'], new_engine)
        
    def test_generate_text(self):
        prompt = "The meaning of life is"
        response = self.client.generate_text(prompt, max_tokens=10)
        self.assertTrue(isinstance(response, str))
         
    #def test_get_fine_tune(self):
        #fine_tune_id = "INSERT_FINE_TUNE_ID_HERE"
        #response = self.client.get_fine_tune(fine_tune_id)
        #self.assertTrue(isinstance(response, dict))
        #self.assertTrue("object" in response.keys())
        #self.assertEqual(response["object"], "fine-tune")
        
    #def test_cancel_fine_tune(self):
        #fine_tune_id = "INSERT_FINE_TUNE_ID_HERE"
        #response = self.client.cancel_fine_tune(fine_tune_id)
        #self.assertTrue(isinstance(response, dict))
        #self.assertTrue("object" in response.keys())
        #self.assertEqual(response["object"], "fine-tune")
        
    #def test_list_fine_tune_events(self):
        #fine_tune_id = "INSERT_FINE_TUNE_ID_HERE"
        #response = self.client.list_fine_tune_events(fine_tune_id, stream=False)
        #self.assertTrue(isinstance(response, dict))
        #self.assertTrue("object" in response.keys())
        #self.assertEqual(response["object"], "list")
        
    #def test_delete_fine_tune_model(self):
        #model = "INSERT_MODEL_ID_HERE"
        #response = self.client.delete_fine_tune_model(model)
        #self.assertTrue(isinstance(response, dict))
        #self.assertTrue("object" in response.keys())
        #self.assertEqual(response["object"], "model")
        
    def test_classify_moderation(self):
        input_text = "I want to kill them"
        response = self.client.classify_moderation(input_text)
        self.assertTrue(isinstance(response, dict))
        self.assertTrue("results" in response.keys())
        self.assertTrue(isinstance(response["results"], list))
        
if __name__ == '__main__':
    unittest.main()

