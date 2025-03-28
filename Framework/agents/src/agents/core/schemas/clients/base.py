"""
This module defines the base classes for LLM clients.
"""
from pydantic import BaseModel
from pydantic_settings import BaseSettings


class Message(BaseModel):
    """
    A Message is a message in a conversation
    """
    role: str
    content: str


class SystemMessage(Message):
    """
    A SystemMessage is a message from the system
    """
    role: str = "system"


class UserMessage(Message):
    """
    A UserMessage is a message from the user
    """
    role: str = "user"
    images: list[str] | None = None


class AssistantMessage(Message):
    """
    An AssistantMessage is a message from the assistant
    """
    role: str = "assistant"


class ClientConfig(BaseSettings):
    """
    A ClientConfig is a configuration for an LLM client
    """
    pass


class ClientRequest(BaseModel):
    """
    A ClientRequest is a request to an LLM client
    """
    messages: list[Message]


class ClientResponse(BaseModel):
    """
    A ClientResponse is a response from an LLM client
    """
    pass


class Client(BaseModel):
    """
    A Client is an LLM-Wrapper Interface
    """
    config: ClientConfig

    def send_request(self, request: ClientRequest) -> ClientResponse:
        """
        Send a request to the LLM client and return the response
        """
        pass

