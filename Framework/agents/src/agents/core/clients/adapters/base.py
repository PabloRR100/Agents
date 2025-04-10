from abc import abstractmethod, ABC
from typing import Generic, TypeVar

from pydantic import BaseModel

import importlib
import pkgutil
from agents.core.clients import ClientResponse
import agents.core.clients.adapters as adapters_pkg


T = TypeVar("T", bound=BaseModel)  # raw response type


class Adapter(ABC, Generic[T]):
    """
    Adapter is a wrapper around the LLM client.
    """
    provider: str
    @staticmethod
    @abstractmethod
    def parse_response(response: T) -> ClientResponse:
        """
        Parse the response and convert it to a format that the LLM client can understand.
        """
        raise NotImplementedError


def discover_adapters():
    for _, name, _ in pkgutil.iter_modules(adapters_pkg.__path__):
        importlib.import_module(f"{adapters_pkg.__name__}.{name}")


_ADAPTER_REGISTRY: dict[str, type[Adapter]] = {}


def register_adapter(cls: type[Adapter]) -> type[Adapter]:
    if not hasattr(cls, "provider"):
        raise ValueError(f"Adapter {cls.__name__} must define a `provider` class attribute.")
    _ADAPTER_REGISTRY[cls.provider] = cls
    return cls

def load_adapter(provider: str) -> Adapter:
    if provider not in _ADAPTER_REGISTRY:
        raise ValueError(f"No adapter registered for provider: {provider}")
    return _ADAPTER_REGISTRY[provider]()



if __name__ == "__main__":

    adapter = load_adapter("openai")
    # assert isinstance(adapter, openai.OpenAIAdapter)


