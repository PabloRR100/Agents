import requests
from typing import Literal

from agents.core.clients import BaseClient, ClientRequest, ClientResponse, ClientConfig
from agents.core.clients.adapters import Adapter


class Client(BaseClient):
    """
    GenericClient does not use any framework it just uses requests to send the request to the LLM.
    """
    provider: Literal["openai", "lmstudio", "ollama"]
    config: ClientConfig
    adapter: Adapter | None = None

    def load_adapter(self):
        self.adapter = Adapter

    @staticmethod
    def _parse_request(request: dict) -> ClientRequest:
        return ClientRequest(**request)

    @staticmethod
    def _parse_response(response: requests.Response) -> ClientResponse:
        return ClientResponse.from_assistant_response(
            assistant_message=response.json().get("message", ""),
            metadata=response.json().get("metadata", None)
        )

    def _send_request(self, request: ClientRequest) -> dict:
        """
        Send a request to the LLM client and return the response.
        This method can be overridden by subclasses to provide specific functionality.
        """
        data = self._parse_request(request)
        response = requests.post(self.config.endpoint_url, json=data)
        response = self._parse_response(response)
        return response

    def solve_request(self, request: dict) -> ClientResponse:
        """
        Run the client with the given request.
        """
        return self._send_request(request)



if __name__ == "__main__":

    client = Client(
        adapter=Adapter("openai"),
        config=ClientConfig(
            llm_name="llama-3.2-3b-instruct",
            endpoint_url="http://localhost:11434"
        )
    )

    question = "What is the capital of France?"
    client_request = ClientRequest.from_user_message(question)
    client_response = client._send_request(**client_request.model_dump())
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