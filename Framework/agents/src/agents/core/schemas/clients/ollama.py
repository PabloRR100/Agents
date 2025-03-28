from pydantic import BaseModel, model_validator
from ollama import Client, ChatResponse

from agents.core.schemas.clients.base import Client, ClientConfig


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
    config: OllamaClientConfig
    endpoint_url: str

    @model_validator(mode="wrap")
    def initialize_client(cls, values):
        """
        Initialize the Ollama client with the provided configuration.
        """
        config = values.get('config')
        if config:
            values['endpoint_url'] = config.endpoint_url
            # Initialize the Ollama client here if needed
            # For example, you can set up authentication or other configurations
        return values

    def send_request(self, request):
        """
        Send a request to the Ollama API and return the response.
        """
        # Implement the logic to send a request to the Ollama API using the provided configuration
        pass


if __name__ == "__main__":

    # Example usage
    config = OllamaClientConfig()
    client = Ollama(config=config)
    response = client.send_request({"prompt": "Hello, world!"})
    print(response)