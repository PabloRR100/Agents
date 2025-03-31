import requests
from typing import Literal

from agents.core.clients import Client, ClientRequest, ClientResponse, ClientConfig


class GenericClient(Client):
    """
    GenericClient does not use any framework it just uses requests to send the request to the LLM.
    """
    provider: Literal["generic"]
    config: ClientConfig

    @staticmethod
    def prepare_request(request: ClientRequest) -> dict:
        return request.model_dump()

    @staticmethod
    def parse_response(response: requests.Response) -> ClientResponse:
        return ClientResponse.from_assistant_response(
            assistant_message=response.json().get("message", ""),
            metadata=response.json().get("metadata", None)
        )

    def send_request(self, request: ClientRequest) -> ClientResponse:
        """
        Send a request to the LLM client and return the response.
        This method can be overridden by subclasses to provide specific functionality.
        """
        data = self.prepare_request(request)
        response = requests.post(self.config.endpoint_url, json=data)
        response = self.parse_response(response)
        return response



if __name__ == "__main__":

    client = GenericClient(
        provider="generic",
        config=ClientConfig(
            llm_name="llama-3.2-3b-instruct",
            endpoint_url="http://localhost:11434"
        )
    )

    question = "What is the capital of France?"
    client_request = ClientRequest.from_user_message(question)
    client_response = client.send_request(client_request)
    print(client_response.assistant_response)

    """
    curl -L -X POST http://127.0.0.1:1234/v1/completions -d '{"model": "llama-3.2-3b-instruct", "prompt": "What is the capital of France?"}' 
    
    curl -L -X POST http://127.0.0.1:1234/v1/completions \
          -H "Content-Type: application/json" \
          -d '{
            "model": "llama-3.2-3b-instruct",
            "prompt": "What is the capital of France?",
            "max_tokens": 100,
            "temperature": 0.7
          }'

    """