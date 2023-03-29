import openai
import requests
import json
from api_key_file import ApiKeyFile
from openai import OpenAIError
#from openai import OpenAIAPIException

class ChatGPTClient:
    def __init__(self, api_key):
        self.api_key = api_key
        self.endpoint = "https://api.openai.com/v1/"
        self.model_engine = "text-davinci-002"
        openai.api_key = self.api_key

        self.chat_history = []
        
    def prompt(self, prompt, **kwargs):
        """
        Prompts the GPT-3 model with the given text and returns the generated response.
        
        Args:
            prompt (str): The text prompt to send to the model.
            **kwargs: Additional keyword arguments to pass to the OpenAI API. 
                      See the API documentation for available options.
            
        Returns:
            A string containing the generated text response from the model.
        """
        prompt_response = openai.Completion.create(
            engine=self.model_engine,
            prompt=prompt,
            **kwargs,
            n=1,
            stop=None,
            temperature=0.7,
        )
        if prompt_response.choices[0].text:
            return prompt_response.choices[0].text.strip()
        else:
            return ""
        
    def completions(self, prompt, max_tokens=100, temperature=0.5, top_p=1, frequency_penalty=0, presence_penalty=0, stop=None, echo=False, n=None, stream=False, logprobs=None, engine=None):
        """
        Generates text completions for a given prompt using the OpenAI API.

        Args:
            **kwargs: Additional parameters to send to the API. See the API documentation for details.

        Returns:
            A list of completion objects returned by the API.
        """
        
        # Build the request data.
        data = {"prompt": prompt, "max_tokens": max_tokens, "temperature": temperature, "top_p": top_p, "frequency_penalty": frequency_penalty, "presence_penalty": presence_penalty}
        if stop is not None:
            data["stop"] = stop
        if echo:
            data["echo"] = echo
        if n is not None:
            data["n"] = n
        if stream:
            data["stream"] = stream
        if logprobs is not None:
            data["logprobs"] = logprobs
        if engine is not None:
            data["engine"] = engine

        data["model"] = self.model_engine

        #data.update(kwargs)

        # Send the API request.
        response = requests.post(
            f"{self.endpoint}completions", 
            headers={"Content-Type": "application/json", "Authorization": f"Bearer {self.api_key}"},
            json=data,
        )

        if not response.ok:
            print(response.request.body)
            print(response.content.decode())

        response.raise_for_status()

        # Extract and return the completions.
        completions = response.json()["choices"]
        return completions

    def set_engine(self, engine):
        """
        Sets the GPT-3 model engine to use for generating responses.

        Args:
            engine (str): The ID of the engine to use.

        Returns:
            None
        """
        self.model_engine = engine

    def get_engine(self):
        """
        Get information about the currently set model engine.

        Returns:
            A dictionary containing information about the currently set model engine.
        """
        url = self.endpoint + "engines/" + self.model_engine
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + self.api_key
        }
        response = requests.get(url, headers=headers)
        return response.json() 

    def add_to_chat_history(self, message):
        self.chat_history.append(message)

    def get_chat_history(self):
        return self.chat_history

    def generate_text(self, prompt, max_tokens, **kwargs):
        """
        Generates text completions given a prompt.

        Args:
            prompt (str): The prompt(s) to generate completions for, encoded as a string, array of strings, array of tokens, or array of token arrays.
            max_tokens (int): The maximum number of tokens to generate in the completion.
            **kwargs: Additional parameters to pass to the OpenAI API, such as engine, temperature, and others.

        Returns:
            str: The generated text completion(s).

        Raises:
            OpenAIError: If an error is returned by the OpenAI API.
        """
        # Define the API endpoint for generating completions
        endpoint = self.endpoint + "engines/" + self.model_engine + "/completions"

        # Define the request headers
        headers = {"Content-Type": "application/json", "Authorization": f"Bearer {self.api_key}"}

        # Define the request data
        data = {
            "prompt": prompt,
            "max_tokens": max_tokens,
        }

        # Merge the additional kwargs into the request data
        data.update(kwargs)

        # Send the API request to generate text completions
        response = requests.post(endpoint, headers=headers, json=data)

        # If the response is not ok, raise an exception
        if not response.ok:
            raise OpenAIError(response.text)

        # Parse the response JSON to get the generated text completion(s)
        response_json = response.json()
        completions = response_json["choices"][0]["text"]

        return completions
    
    
    def get_fine_tune(self, fine_tune_id):
        """
        Retrieve information about a fine-tuned model.
        """
        url = self.endpoint + f"fine-tunes/{fine_tune_id}"
        headers = {"Authorization": f"Bearer {self.api_key}"}
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        return response.json()
       
    def cancel_fine_tune(self, fine_tune_id):
        """
        Immediately cancels a fine-tune job.

        Args:
        - fine_tune_id (str): The ID of the fine-tune job to cancel

        Returns:
        A dictionary with the updated status of the fine-tune job.
        """
        url = self.endpoint + f"fine-tunes/{fine_tune_id}/cancel"
        headers = {"Authorization": f"Bearer {self.api_key}"}
        response = requests.post(url, headers=headers)
        response.raise_for_status()
        return response.json()

    def list_fine_tune_events(self, fine_tune_id, stream=False):
        """
        Get fine-grained status updates for a fine-tune job.

        Args:
            fine_tune_id (str): The ID of the fine-tune job to get events for.
            stream (bool, optional): Whether to stream events for the fine-tune job. If set to true, events
                will be sent as data-only server-sent events as they become available. The stream will terminate
                with a data: [DONE] message when the job is finished (succeeded, cancelled, or failed).
                If set to false, only events generated so far will be returned. Defaults to False.

        Returns:
            dict: A dictionary containing the fine-tune events.

        Raises:
            OpenAIError: If the request fails for any reason.
        """
        url = f"{self.endpoint}fine-tunes/{fine_tune_id}/events"

        params = {
            "stream": stream
        }

        response = requests.get(url, headers=self.get_headers(), params=params)

        if response.status_code != 200:
            raise OpenAIError(f"Request failed with code {response.status_code}. Message: {response.json()['error']}")

        return response.json() 

    def delete_fine_tune_model(self, model):
        """
        Delete a fine-tuned model.
        :param model: The ID of the model to delete.
        :return: Returns True if the model was deleted successfully.
        """
        url = f"{self.endpoint}models/{model}"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }
        response = requests.delete(url, headers=headers)
        response.raise_for_status()

        return response.json().get("deleted", False)
 
    def classify_moderation(self, input_text, model="text-moderation-latest"):
        """
        Classify if a given input text violates OpenAI's content policy using the text moderation API.

        :param input_text: The input text to classify.
        :type input_text: str
        :param model: The moderation model to use. Defaults to "text-moderation-latest".
        :type model: str
        :return: The classification result as a dictionary.
        :rtype: dict
        """

        url = self.endpoint + "moderations"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        data = {
            "input": input_text,
            "model": model
        }
        response = requests.post(url, headers=headers, json=data)

        return response.json()

if __name__ == "__main__":
    api_key_file = ApiKeyFile()
    api_key = api_key_file.get_api_key()
    client = ChatGPTClient(api_key)
    print(client.get_engine())
    # Use client methods here

