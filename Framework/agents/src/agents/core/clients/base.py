"""
This module defines the base classes for LLM clients.
"""
from abc import ABC
from typing import TypeVar

from pydantic import BaseModel, ConfigDict, model_validator

from agents.core.schemas.messages import Message, UserMessage, AssistantMessage, Tool


ClientType = TypeVar("ClientType", bound="Client")
OutputSchema = TypeVar("OutputSchema", bound=BaseModel)


class ClientConfig(BaseModel):
    """
    A ClientConfig is a configuration for an LLM client
    """
    llm_name: str
    endpoint_url: str


class ClientRequestMetadata(BaseModel):
    """




    Metadata for a ClientRequest
    """
    output_schema: bool | None = OutputSchema
    constrained_decoding: bool | None = False

    @model_validator(mode="before")
    def validate_metadata(cls, values):
        """
        Validate the metadata for the ClientRequest.
        This can be used to set default values or validate the input.
        """
        if values.get("constrained_decoding", None) :
            # Constrained Decoding requires an output schema to be defined
            if values.get("output_schema", None) is None:
                # If constrained decoding is enabled, output_schema must be defined
                raise ValueError("When constrained_decoding is enabled, output_schema must be defined.")
        return values


class ClientRequest(BaseModel):
    """
    A ClientRequest is a request to an LLM client
    """
    messages: list[Message]
    tools: list[Tool] | None = None
    metadata: ClientRequestMetadata | None = None

    @classmethod
    def from_user_message(cls, user_message: str) -> "ClientRequest":
        return cls(
            messages=[UserMessage(content=user_message)]
        )

    def get_last_user_message(self) -> Message | None:
        """
        Get the last user message from the ClientRequest.
        """
        user_messages = [msg for msg in self.messages if isinstance(msg, UserMessage)]
        if user_messages:
            return user_messages[-1]
        return None


class ClientResponseMetadata(BaseModel):
    """
    Metadata for a ClientResponse.
    Useful to store additional information about the response, like the usage
    """
    model_config = ConfigDict(extra="allow")


class ClientResponse(BaseModel):
    """
    A ClientResponse is a response from an LLM client
    """
    message: AssistantMessage | None = None
    metadata: ClientResponseMetadata | None = None

    @classmethod
    def from_assistant_response(cls, assistant_message: str, metadata: dict | None = None):
        return cls(
            message=AssistantMessage(content=assistant_message),
            metadata=metadata
        )

    @property
    def assistant_response(self) -> str:
        return self.message.content


class BaseClient(ABC, BaseModel):
    """
    A Client is an LLM-Wrapper Interface.
    """
    provider: str
    config: ClientConfig

    model_config = ConfigDict(arbitrary_types_allowed=True)

    def solve_request(self, request: dict) -> ClientResponse:
        """
        Run the client with the given request.
        """
        raise NotImplementedError

    # @staticmethod
    # def _parse_request(request: dict) -> ClientRequest:
    #     """
    #     Parse the request and convert it to a format that the LLM client can understand.
    #     """
    #     raise NotImplementedError
    #
    # @staticmethod
    # def _parse_response(response: dict) -> ClientResponse:
    #     """
    #     Parse the request and convert it to a format that the LLM client can understand.
    #     """
    #     raise NotImplementedError
    #
    # @abstractmethod
    # def _send_request(self, request: ClientRequest) -> dict:
    #     """
    #     Send a request to the LLM client and return the response
    #     """
    #     raise NotImplementedError