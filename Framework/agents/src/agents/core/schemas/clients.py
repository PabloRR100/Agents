from pydantic import BaseModel
from pydantic_settings import BaseSettings


class ClientConfig(BaseSettings):
    """
    A ClientConfig is a configuration for an LLM client
    """
    pass


class ClientRequest(BaseModel):
    """
    A ClientRequest is a request to an LLM client
    """
    pass


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

