from typing import Literal

import lmstudio as lms
from pydantic import model_validator

from agents.core.clients import ClientRequest, ClientResponse
from agents.core.clients.base import BaseClient, ClientConfig


class LMStudioClientConfig(ClientConfig):
    """
    Configuration for the Ollama client.
    """
    # Add any specific configuration fields for the Ollama client here
    llm_name: str
    endpoint_url: str


class LMStudio(BaseClient):
    """
    LMStudio client for interacting with the Ollama API.
    """
    provider: Literal["lmstudio"]
    config: LMStudioClientConfig

    @model_validator(mode="before")
    def initialize_client(cls, values: dict) -> dict:
        """
        Initialize the Ollama client with the provided configuration.
        """
        return values

    @staticmethod
    def _parse_request(request: ClientRequest) -> lms.Chat:
        """
        Parse the ClientRequest and convert it to a format that the LMStudio API can understand.
        """
        # Create a chat history object for the Ollama API
        chat_history = lms.Chat()

        # Iterate through the messages in the request and add them to the chat history
        for message in request.messages:
            if message.role == "user":
                chat_history.add_user_message(message.content)
            elif message.role == "assistant":
                chat_history.add_assistant_response(message.content)
        return chat_history

    @staticmethod
    def _parse_response(response: lms.PredictionResult) -> ClientResponse:
        """
        Parse the response from the Ollama API and convert it to a ClientResponse.
        """
        # Assuming the response from the model is a string or a format that can be converted to a ClientResponse
        # You may need to adjust this based on the actual response structure
        client_response = ClientResponse.from_assistant_response(response.content)
        return client_response

    def _send_request(self, request: ClientRequest) -> ClientResponse:
        """
        Send a request to the Ollama API and return the response.
        """
        model_request = self._parse_request(request)
        try:
            with lms.Client() as client:
                model = client.llm.model()
                model_response = model.respond(model_request)
            client_response = self._parse_response(model_response)
            return client_response

        except Exception as e:
            raise e


if __name__ == "__main__":

    # Example usage
    sample_config = {
        "provider": "lmstudio",
        "config":  {
            "llm_name": "olympiccoder-7b",
            "endpoint_url": "http://localhost:11434/"
        }
    }
    sample_client = LMStudio(config=sample_config)

    sample_request = {
        "messages": [
            {
                "role": "user",
                "content": "Hello!"
            }
        ]
    }
    sample_request = ClientRequest(**sample_request)  # Convert the dictionary to a ClientRequest object
    sample_response = sample_client._send_request(request=sample_request)
    print(sample_response)