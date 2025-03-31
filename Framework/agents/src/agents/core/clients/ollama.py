from typing import Literal

from pydantic import model_validator

from agents.core.clients.base import Client, ClientConfig


class OllamaClientConfig(ClientConfig):
    """
    Configuration for the Ollama client.
    """
    # Add any specific configuration fields for the Ollama client here
    llm_name: str = "llama2"
    endpoint_url: str = "http://localhost:11434/v1/chat/completions"


class Ollama(Client):
    """
    Ollama client for interacting with the Ollama API.

    Example of Ollama:
        client = Client(
            host='http://localhost:11434',
            headers={'x-some-header': 'some-value'}
        )
        response = client.chat(model='llama3.2', messages=[
            {
                'role': 'user',
                'content': 'Why is the sky blue?',
            },
        ])
    """
    provider: Literal["ollama"]
    config: OllamaClientConfig

    @model_validator(mode="before")
    def initialize_client(cls, values: dict) -> dict:
        """
        Initialize the Ollama client with the provided configuration.
        """
        config = values.get('config')
        return config
