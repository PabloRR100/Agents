import yaml

from pydantic import Field, TypeAdapter
from typing import Union, Annotated

from .base import BaseClient
from agents.core.clients.sdks.gemini import Gemini
from agents.core.clients.sdks.lms import LMStudio
from .ollama import Ollama


ClientUnion = Annotated[
    Union[Gemini, LMStudio, Ollama],
    Field(discriminator="provider")
]

DEFAULT_CONFIG = {
    "provider": "gemini"
}

class ClientLoader:

    @staticmethod
    def load(
        config: dict | None = None
    ) -> BaseClient:
        if not config:
            config = DEFAULT_CONFIG
        resolved_client = TypeAdapter(ClientUnion).validate_python(config)
        return resolved_client

    @classmethod
    def load_client_from_yaml(cls, path: str) -> BaseClient:
        with open(path) as f:
            data = yaml.safe_load(f)
            return cls.load(config=data["client"])


if __name__ == "__main__":

    # Example usage
    loader = ClientLoader()
    client = loader.load_client_from_yaml("path/to/client_config.yaml")
    print(client)